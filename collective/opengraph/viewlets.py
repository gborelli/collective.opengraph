from Acquisition import aq_inner

from zope.app.pagetemplate.viewpagetemplatefile import ViewPageTemplateFile
from plone.app.layout.viewlets import ViewletBase

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


class OGPViewlet(ViewletBase):
    template = ViewPageTemplateFile('ogpviewlet.pt')
    img_size = IMG_SIZE

    def render(self):
        return self.template()

    @property
    def default_charset(self):
        pt = self.context.restrictedTraverse('@@plone_tools')
        portal_prop = pt.properties()
        return portal_prop.site_properties.default_charset

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
        return  decode_str(self.context.Title(), self.default_charset)

    @property
    def sitename(self):
        sitename = self.portal_state.portal().Title()
        return decode_str(sitename, self.default_charset)
