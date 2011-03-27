# -*- coding: utf-8 -*-
import unittest2 as unittest
from zope.component import queryMultiAdapter
from zope.component import getAdapters
from zope.interface import directlyProvides
from zope.viewlet.interfaces import IViewletManager, IViewlet

from Products.Five.browser import BrowserView
from plone.browserlayer import utils
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID

from collective.opengraph.interfaces import IBrowserLayer
from collective.opengraph.viewlets import IMG_SIZE
from layer import OPENGRAPH_INTEGRATION_TESTING


VIEWLET_NAME = 'collective.opengraph.meta'
NEWS_TITLE = u"Test News"
NEWS_DESCRIPTION = u"Document news"
DOCUMENT_TITLE = u"Test Document"
DOCUMENT_DESCRIPTION = u"Document description"


def loadImage(name, size=0):
    """Load image from testing directory
    """
    import os
    dir_name = os.path.dirname(__file__)
    path = os.path.join(dir_name, 'input', name)
    fd = open(path, 'rb')
    data = fd.read()
    fd.close()
    return data


class OpenGraphViewletTests(unittest.TestCase):
    layer = OPENGRAPH_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        directlyProvides(self.request, IBrowserLayer)

        # we create some test content
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        doc_id = self.portal.invokeFactory('Document', 'test_document',
                    title=DOCUMENT_TITLE, description= DOCUMENT_DESCRIPTION)
        self.document = self.portal[doc_id]
        news_id = self.portal.invokeFactory('News Item', 'test_news',
                    title=NEWS_TITLE, description= NEWS_DESCRIPTION)
        self.news = self.portal[news_id]
        setRoles(self.portal, TEST_USER_ID, ['Member'])

    def _get_viewlets(self, context, manager_name):
        view = BrowserView(self.portal, self.request)
        manager = queryMultiAdapter((context, self.request, view),
                                IViewletManager, name=manager_name)
        viewlets = getAdapters((manager.context, manager.request,
                                      manager.__parent__, manager), IViewlet)
        viewlets_dict = {}
        for name, viewlet in viewlets:
            viewlets_dict[name] = viewlet
        return viewlets_dict

    def testBrowserLayer(self):
        self.assertTrue(IBrowserLayer in utils.registered_layers())

    def testViewlet(self):
        viewlets = self._get_viewlets(self.portal, 'plone.htmlhead.links')
        self.assertTrue(VIEWLET_NAME in viewlets.keys())

    def testDocumentViewlet(self):
        viewlets = self._get_viewlets(self.document, 'plone.htmlhead.links')
        opengraph_viewlet = viewlets[VIEWLET_NAME]
        opengraph_viewlet.update()
        html = opengraph_viewlet.render()

        self.assertTrue(u'<meta property="og:title" content="%s" />' \
                                        % DOCUMENT_TITLE in html)
        self.assertTrue(u'<meta property="og:url" content="%s" />' \
                                        % self.document.absolute_url() in html)
        self.assertTrue(u'<meta property="og:image" content="%s/logo.jpg" />' \
                                        % self.portal.absolute_url() in html)
        self.assertTrue(u'<meta property="og:site_name" content="%s" />' \
                                        % self.portal.Title() in html)
        self.assertTrue(u'<meta property="og:description" content="%s" />' \
                                        % DOCUMENT_DESCRIPTION in html)

    def testNewsViewlet(self):
        viewlets = self._get_viewlets(self.news, 'plone.htmlhead.links')
        opengraph_viewlet = viewlets[VIEWLET_NAME]
        opengraph_viewlet.update()
        html = opengraph_viewlet.render()

        self.assertTrue(u'<meta property="og:title" content="%s" />' \
                                        % NEWS_TITLE in html)
        self.assertTrue(u'<meta property="og:url" content="%s" />' \
                                        % self.news.absolute_url() in html)
        self.assertTrue(u'<meta property="og:image" content="%s/logo.jpg" />' \
                                        % self.portal.absolute_url() in html)
        self.assertTrue(u'<meta property="og:site_name" content="%s" />' \
                                        % self.portal.Title() in html)
        self.assertTrue(u'<meta property="og:description" content="%s" />' \
                                        % NEWS_DESCRIPTION in html)

    def testNewsImageViewlet(self):
        # we set an image in News Item
        TEST_GIF = loadImage('test.gif')
        self.news.setImage(TEST_GIF, mimetype='image/gif', filename='test.gif')

        viewlets = self._get_viewlets(self.news, 'plone.htmlhead.links')
        opengraph_viewlet = viewlets[VIEWLET_NAME]
        opengraph_viewlet.update()
        html = opengraph_viewlet.render()

        self.assertTrue(
                u'<meta property="og:image" content="%s/image_%s" />' \
                    % (self.news.absolute_url(), IMG_SIZE) in html)


def test_suite():
    from unittest import defaultTestLoader
    return defaultTestLoader.loadTestsFromName(__name__)
