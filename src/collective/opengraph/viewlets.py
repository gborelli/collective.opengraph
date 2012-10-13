from Acquisition import aq_inner
from zope.interface import implements
from zope.component import getUtility
from zope.app.pagetemplate.viewpagetemplatefile import ViewPageTemplateFile
from ordereddict import OrderedDict

from plone.app.layout.viewlets import ViewletBase
from plone.registry.interfaces import IRegistry

from collective.opengraph.interfaces import IOpengraphSettings, IOpengraphMetatags

IMG_SIZE = 'thumb'
HAS_LEADIMAGE = True
try:
    from collective.contentleadimage.config import IMAGE_FIELD_NAME
except:
    HAS_LEADIMAGE = False


def decode_str(val, encoding):
    if isinstance(val, unicode):
        return val
    return unicode(val, 'utf8')


class LastUpdatedOrderedDict(OrderedDict):
    'Store items in the order the keys were last added'

    def __setitem__(self, key, value):
        if key in self:
            del self[key]
        OrderedDict.__setitem__(self, key, value)


class ATMetatags(object):

    implements(IOpengraphMetatags)
    img_size = IMG_SIZE

    def __init__(self, context):
        self.context = context
        self.portal_state = self.context.restrictedTraverse('@@plone_portal_state')

    @property
    def default_charset(self):
        pt = self.context.restrictedTraverse('@@plone_tools')
        portal_prop = pt.properties()
        return portal_prop.site_properties.default_charset

    @property
    def settings(self):
        registry = getUtility(IRegistry)
        return registry.forInterface(IOpengraphSettings)

    @property
    def metatags(self):
        tags = LastUpdatedOrderedDict()
        tags.update([('og:title', self.title),
                     ('og:url', self.context.absolute_url()),
                     ('og:image', self.image_url),
                     ('og:site_name', self.sitename),
                     ('og:description', self.description)])
	if self.content_type:
            tags.update({'og:type' : self.content_type})
        if self.admins:
            tags.update({'fb:admins' : self.admins})
        if self.app_id:
            tags.update({'fb:app_id' : self.app_id})
	return tags

    @property
    def image_url(self):
        """Return an image url for the context in that order
        - context image field
        - context lead image field
        - portal logo
        """
        context = aq_inner(self.context)
        obj_url = context.absolute_url()
        if hasattr(context, 'getField'):
            field = self.context.getField('image')
            if not field and HAS_LEADIMAGE:
                field = context.getField(IMAGE_FIELD_NAME)

            if field and field.get_size(context) > 0:
                return u'%s/%s_%s' % (obj_url, field.getName(), self.img_size)

        return "%s/logo.jpg" % self.portal_state.portal_url()

    @property
    def description(self):
        return decode_str(self.context.Description(), self.default_charset)

    @property
    def title(self):
        return decode_str(self.context.Title(), self.default_charset)

    @property
    def sitename(self):
        sitename = self.portal_state.portal().Title()
        return decode_str(sitename, self.default_charset)
    
    @property
    def content_type(self):
        default_type = self.settings.default_type or ''
        return decode_str(default_type, self.default_charset)

    @property
    def admins(self):
        admins = self.settings.admins or ''
        return decode_str(admins, self.default_charset)

    @property
    def app_id(self):
        appid = self.settings.app_id or ''
        return decode_str(appid, self.default_charset)


class OGViewlet(ViewletBase):
    template = ViewPageTemplateFile('ogviewlet.pt')

    def render(self):
        return self.template()

    def metatags(self):
        return IOpengraphMetatags(self.context).metatags.items()

