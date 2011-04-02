from zope import schema
from zope.interface import Interface
from plone.theme.interfaces import IDefaultPloneLayer

from collective.opengraph import OpengraphMessageFactory as _


class IBrowserLayer(IDefaultPloneLayer):
    """Marker interface that defines a Zope 3 browser layer.
    """


class IOpengraphable(Interface):
    """Marker interface for opengraph content types
    """


class IOpengraphSettings(Interface):
    """Opengraph default settings
    """

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
    pass

class IOpengraphMarker(Interface):
    pass

