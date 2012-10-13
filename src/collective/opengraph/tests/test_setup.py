# -*- coding: utf-8 -*-
import unittest2 as unittest
from zope.schema.vocabulary import SimpleVocabulary
from zope.schema.interfaces import IVocabularyFactory
from zope.component import getUtility
from zope.component import queryUtility

from plone.browserlayer import utils
from plone.registry.interfaces import IRegistry

from collective.opengraph.interfaces import IBrowserLayer
from collective.opengraph.interfaces import IOpengraphSettings

from layer import OPENGRAPH_INTEGRATION_TESTING


SETTINGS_PROPS = ['default_type', 'types']  # , 'content_types']


class OpenGraphSetupTests(unittest.TestCase):
    layer = OPENGRAPH_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']

    @property
    def _registry(self):
        return getUtility(IRegistry)

    def testBrowserLayer(self):
        self.assertTrue(IBrowserLayer in utils.registered_layers())

    def testVocabulary(self):
        vocabulary = queryUtility(IVocabularyFactory,
                        name="collective.opengraph.types")
        self.assertIsNotNone(vocabulary)
        vocabulary = vocabulary(None)
        self.assertTrue(isinstance(vocabulary, SimpleVocabulary))

        terms = ['website', 'article']
        for item in terms:
            self.assertEquals(vocabulary.getTerm(item).value, item)

    def testSettings(self):
        settings = self._registry.forInterface(IOpengraphSettings)
        for prop in SETTINGS_PROPS:
            self.assertTrue(hasattr(settings, prop))

        self.assertEquals(len(settings.types), 38)


def test_suite():
    from unittest import defaultTestLoader
    return defaultTestLoader.loadTestsFromName(__name__)
