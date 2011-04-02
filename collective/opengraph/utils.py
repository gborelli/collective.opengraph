from zope.interface import implements, alsoProvides, noLongerProvides
from zope.component import getUtility
from zope.component import queryUtility
from Products.CMFCore.utils import getToolByName

from plone.registry.interfaces import IRegistry

from collective.opengraph.interfaces import IOpengraphable
from collective.opengraph.interfaces import IOpengraphMarker
from collective.opengraph.interfaces import IOpengraphMarkerUtility
from collective.opengraph.interfaces import IOpengraphSettings

from collective.opengraph import OpengraphMessageFactory as _


def opengraph_settings(context):
    return getUtility(IRegistry).forInterface(IOpengraphSettings)


def update_opengraphable_objects(context, new_ct):
    g_marker = queryUtility(IOpengraphMarkerUtility)
    if not g_marker:
        return

    ct = getToolByName(context, 'portal_catalog')
    query = {'object_provides':
                'collective.opengraph.interfaces.IOpengraphable'}
    pt = [item.portal_type for item in ct.searchResults(query)]
    olds_pt = list(set(pt))

    adds = []
    for new in new_ct:
        if new in olds_pt:
            olds_pt.remove(new)
        else:
            adds.append(new)
    if len(olds_pt)==0 and len(adds)==0:
        return

    nb_items, bad_items = g_marker.update(context, adds, olds_pt)
    updated = u'%d %s' % (nb_items, _(u'objects updated.'))
    if not bad_items:
        message = updated
    else:
        message = u'%s, %d %s: %s' % (updated,
                                      len(bad_items),
                                      _(u'update(s) on object(s) failed'),
                                      ','.join(bad_items), )
    pu = getToolByName(context, 'plone_utils')
    pu.addPortalMessage(message)


class OpengraphMarker(object):
    """ Utility to mark an object IOpengraphable
    """
    implements(IOpengraphMarker)

    def __init__(self, context):
        self.context = context

    @property
    def _options(self):
        return opengraph_settings(self.context)

    @property
    def opengraphable_types(self):
        """ Return the georeferenceable portal types
        """
        return self._options.types

    def process(self):
        """ Proceed to the markage
        """
        try: 
            opengraphable_types = self.opengraphable_types
        except:
            return

        if not self.context.portal_type in opengraphable_types:
            self.clear()
        else:
            self.add()

    def add(self):
        """ Add the markage
        """
        if IOpengraphable.providedBy(self.context):
            return
        alsoProvides(self.context, IOpengraphable)
        self.context.reindexObject(idxs=['object_provides'])

    def clear(self):
        """ Clear the markage
        """
        if not IOpengraphable.providedBy(self.context):
            return
        noLongerProvides(self.context, IOpengraphable)
        self.context.reindexObject(idxs=['object_provides'])


class OpengraphMarkerUtility(object):
    """
    """
    implements(IOpengraphMarkerUtility)

    def update(self, context, news, olds):
        """ Update only objects with a change of configuration
        """
        i = 0
        bad_objects = []
        for new in news:
            j, bads = self._walker(context, 'add', new)
            i += j
            bad_objects += bads
        for old in olds:
            j, bads = self._walker(context, 'clear', old)
            i += j
            bad_objects += bads
        return i, bad_objects

    def updateAll(self, context):
        """ Update all objects on portal
        """
        return self._walker(context, 'process')

    def _walker(self, context, meth, portal_type = ''):
        """
        """
        pc = getToolByName(context, 'portal_catalog')
        bad_objects = []
        i = 0
        if portal_type != '':
            brains = pc(portal_type=portal_type)
        else:
            brains = pc()

        for brain in brains:
            try:
                process = getattr(IOpengraphMarker(brain.getObject()), meth, None)
                if process != None:
                    process()
                i += 1
            except:
                bad_objects.append(brain.getPath())
                continue
        return i, bad_objects
