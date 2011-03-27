# -*- coding: utf-8 -*-
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import PLONE_FIXTURE, PLONE_FUNCTIONAL_TESTING
from plone.app.testing import IntegrationTesting, FunctionalTesting

# from plone.testing import z2

class OpengraphLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE, )

    def setUpZope(self, app, configurationContext):
        # Load ZCML
        import collective.opengraph
        self.loadZCML(package=collective.opengraph)

        # # questa è una menata non viene richiamato
        # # initialize() e quindi devo farlo a mano
        # z2.installProduct(app, 'abstract.easyshop')
    def setUpPloneSite(self, portal):
        # Install into Plone site using portal_setup
        self.applyProfile(portal, 'collective.opengraph:default')

    def tearDownZope(self, app):
        pass
        # Uninstall product
        # z2.uninstallProduct(app, 'abstract.easyshop')

OPENGRAPH_FIXTURE = OpengraphLayer()
OPENGRAPH_INTEGRATION_TESTING = IntegrationTesting(
                                bases=(OPENGRAPH_FIXTURE, ),
                                name="OpengraphLayer:Integration")

OPENGRAPH_FUNCTIONAL_TESTING = FunctionalTesting(
                                bases=(PLONE_FUNCTIONAL_TESTING, OPENGRAPH_FIXTURE,),
                                name="OpengraphLayer:Functional")
