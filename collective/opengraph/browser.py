from collective.opengraph import OpengraphMessageFactory as _
from collective.opengraph.interfaces import IOpengraphable
from Products.CMFCore.utils import getToolByName
from Products.Five import BrowserView
from zope.interface import alsoProvides
from zope.interface import noLongerProvides


class EnableOpengraph(BrowserView):

    def __call__(self):
        alsoProvides(self.context, IOpengraphable)
        plone_utils = getToolByName(self.context, 'plone_utils')
        plone_utils.addPortalMessage(_(u"The opengraph tags has been enabled"))
        self.request.response.redirect(self.context.absolute_url())


class DisableOpengraph(BrowserView):

    def __call__(self):
        noLongerProvides(self.context, IOpengraphable)
        plone_utils = getToolByName(self.context, 'plone_utils')
        plone_utils.addPortalMessage(_(u"The opengraph tags has been disabled"))
        self.request.response.redirect(self.context.absolute_url())


class OpengraphEnabled(BrowserView):

    @property
    def is_opengraph_enabled(self):
        return IOpengraphable.providedBy(self.context)
