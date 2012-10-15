from zope import schema
from zope.interface import Interface
from plone.theme.interfaces import IDefaultPloneLayer

from collective.opengraph import OpengraphMessageFactory as _


class IBrowserLayer(IDefaultPloneLayer):
    """Marker interface that defines a Zope 3 browser layer.
    """


class IOpengraphable(Interface):
    """
    Marker interface for opengraph content types.
    Used to render the head section og viewlet.
    """

class IOpengraphMetatags(Interface):
    """
    Returns opengraph metadata
    """

    metatags = schema.Dict(
        title = _(u'List of opengraph metatags'),
        required = True,
        default = {},
        description = _(u"A dict of opengraph metatags "
                         "which will be used by the opengraph viewlet"),
	key_type = schema.TextLine(title=u"Metatag name"),
        value_type = schema.TextLine(title=u"Metatag value"))


class IOpengraphSettings(Interface):
    """Opengraph default settings
    """

    app_id = schema.TextLine(
            title=_(u"Facebook app id"),
            required=False)
    
    api_secret = schema.TextLine(
                title=_(u"Facebook api secret"),
                required=False)

    admins = schema.TextLine(
            title=_(u"Admins"),
            required = False)

    default_type = schema.Choice(
            title= _(u"Default type"),
            description = _(u"A default opengraph type metatag"),
            required = True,
            vocabulary = "collective.opengraph.types",
        )

    types = schema.List(
        title = _(u'Type of contents'),
        required = False,
        default = [],
        description = _(u"A list of types which can be selected "
                         "for opengraph type metatag"),
        value_type = schema.TextLine(title=u"Type"))

    content_types = schema.List(
        title = _(u'Content types'),
        required = False,
        description = _(u"A list of types which can be tagged "
                         "by opengraph metatag"),
        value_type = schema.Choice(title=_(u"Content types"),
                    source="plone.app.vocabularies.ReallyUserFriendlyTypes"))


class IOpengraphMarkerUtility(Interface):
    """Utility that handles the configurations."""


class IOpengraphMarker(Interface):
    """Worker that marks with IOpengraphable interface."""

