from zope.interface import implementer
from zope.component import getUtility
from zope.schema.vocabulary import SimpleVocabulary
from zope.schema.interfaces import IVocabularyFactory

from plone.registry.interfaces import IRegistry
from interfaces import IOpengraphSettings


@implementer(IVocabularyFactory)
def opengraphTypesVocab(context):
    def _createterm(term):
        return SimpleVocabulary.createTerm(term, term, term)

    registry = getUtility(IRegistry)
    settings = registry.forInterface(IOpengraphSettings)
    terms = settings.types
    return SimpleVocabulary([_createterm(term) for term in terms])
