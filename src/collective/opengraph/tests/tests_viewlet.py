# -*- coding: utf-8 -*-
import unittest2 as unittest

from zope.component import queryMultiAdapter
from zope.component import getUtility
from zope.component import getAdapters
from zope.interface import directlyProvides
from zope.interface import alsoProvides
from zope.viewlet.interfaces import IViewletManager, IViewlet

from Products.Five.browser import BrowserView
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID

from plone.registry.interfaces import IRegistry

from collective.opengraph.interfaces import IBrowserLayer
from collective.opengraph.interfaces import IOpengraphSettings
from collective.opengraph.interfaces import IOpengraphable
from collective.opengraph.viewlets import IMG_SIZE

from layer import OPENGRAPH_INTEGRATION_TESTING


VIEWLET_NAME = 'collective.opengraph.meta'
NEWS_TITLE = u"Test News"
NEWS_DESCRIPTION = u"Document news"
DOCUMENT_TITLE = u"Test Document"
DOCUMENT_DESCRIPTION = u"Document description"
VIEWLET_HTML = """<meta property="og:title" content="%(title)s" /><meta property="og:url" content="%(url)s" /><meta property="og:image" content="%(image)s" /><meta property="og:site_name" content="%(site_name)s" /><meta property="og:description" content="%(description)s" />"""


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
        alsoProvides(self.document, IOpengraphable)
        news_id = self.portal.invokeFactory('News Item', 'test_news',
                    title=NEWS_TITLE, description= NEWS_DESCRIPTION)
        self.news = self.portal[news_id]
        alsoProvides(self.news, IOpengraphable)
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

    def testViewlet(self):
        viewlets = self._get_viewlets(self.portal, 'plone.htmlhead.links')
        self.assertFalse(VIEWLET_NAME in viewlets.keys())

        alsoProvides(self.portal, IOpengraphable)
        viewlets = self._get_viewlets(self.portal, 'plone.htmlhead.links')
        self.assertTrue(VIEWLET_NAME in viewlets.keys())

    def testDocumentViewlet(self):
        viewlets = self._get_viewlets(self.document, 'plone.htmlhead.links')
        opengraph_viewlet = viewlets[VIEWLET_NAME]
        opengraph_viewlet.update()
        html = opengraph_viewlet.render()

        params = {'title': DOCUMENT_TITLE,
                  'url': self.document.absolute_url(),
                  'image': "%s/logo.jpg" % self.portal.absolute_url(),
                  'site_name': self.portal.Title(),
                  'description': DOCUMENT_DESCRIPTION}
        self.assertEquals((VIEWLET_HTML % params).replace("\n", ''), html.replace("\n", ''))

    def testNewsViewlet(self):
        viewlets = self._get_viewlets(self.news, 'plone.htmlhead.links')
        opengraph_viewlet = viewlets[VIEWLET_NAME]
        opengraph_viewlet.update()
        html = opengraph_viewlet.render()

        params = {'title': NEWS_TITLE,
                  'url': self.news.absolute_url(),
                  'image': "%s/logo.jpg" % self.portal.absolute_url(),
                  'site_name': self.portal.Title(),
                  'description': NEWS_DESCRIPTION}
        self.assertEquals((VIEWLET_HTML % params).replace("\n", ''), html.replace("\n", ''))

    def testNewsImageViewlet(self):
        # we set an image in News Item
        TEST_GIF = loadImage('test.gif')
        self.news.setImage(TEST_GIF, mimetype='image/gif', filename='test.gif')

        viewlets = self._get_viewlets(self.news, 'plone.htmlhead.links')
        opengraph_viewlet = viewlets[VIEWLET_NAME]
        opengraph_viewlet.update()
        html = opengraph_viewlet.render()

        params = {'title': NEWS_TITLE,
                  'url': self.news.absolute_url(),
                  'image': "%s/image_%s" % (self.news.absolute_url(), IMG_SIZE),
                  'site_name': self.portal.Title(),
                  'description': NEWS_DESCRIPTION}
        self.assertEquals((VIEWLET_HTML % params).replace("\n", ''), html.replace("\n", ''))

    def testDefaultTypeViewlet(self):
        default_type = 'article'
        registry = getUtility(IRegistry)
        settings = registry.forInterface(IOpengraphSettings)
        settings.default_type = default_type

        viewlets = self._get_viewlets(self.document, 'plone.htmlhead.links')
        opengraph_viewlet = viewlets[VIEWLET_NAME]
        opengraph_viewlet.update()
        html = opengraph_viewlet.render()

        # params = {'title': DOCUMENT_TITLE,
        #           'url': self.document.absolute_url(),
        #           'image': "%s/logo.jpg" % self.portal.absolute_url(),
        #           'site_name': self.portal.Title(),
        #           'description': DOCUMENT_DESCRIPTION}
        type_html = '<meta property="og:type" content="%s" />' % 'article'
        self.assertTrue(type_html in html)


def test_suite():
    from unittest import defaultTestLoader
    return defaultTestLoader.loadTestsFromName(__name__)
