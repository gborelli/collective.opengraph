from zope.interface import implements
from plone.app.controlpanel.interfaces import IConfigurationChangedEvent
from plone.app.controlpanel.events import ConfigurationChangedEvent
from utils import update_opengraphable_objects


class IOpengraphSettingsEvent(IConfigurationChangedEvent):
    """An event signaling that geo settings are saved
    """


class OpengraphSettingsEvent(ConfigurationChangedEvent):
    implements(IOpengraphSettingsEvent)


def updateOpengraphableObjects(event):
    """update all opengraphable event on change settings
    """
    update_opengraphable_objects(event.context,
                        event.data.get('content_types', []))
