from five import grok
from AccessControl import ClassSecurityInfo
from plone.dexterity.content import IDexterityContent
from plone import api
from interfaces import IColumn

class dt_column(IDexterityContent):
    grok.implements(IColumn)
    security = ClassSecurityInfo()
    def __init__(self):
        IDexterityContent.__init__(IDexterityContent)
        trg = self.aq_parent['columns']
        api.content.move(
            source=self,
            target=trg,
            safe_id=True)

    def __iter__(self):
        for attr, value in self.__dict__.iteritems():
            yield attr, value
