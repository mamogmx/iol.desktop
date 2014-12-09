from five import grok
from AccessControl import ClassSecurityInfo
from plone.dexterity.content import DexterityContent
from plone import api
from interfaces import IColumn
from zope.lifecycleevent.interfaces import IObjectAddedEvent
from Products.CMFCore.utils import getToolByName

class dt_column(DexterityContent):
    #grok.implements(IColumn)
    #security = ClassSecurityInfo()
    #def __init__(self):
    #    DexterityContent.__init__(self)
    #    trg = self.getParentNode()

    #    api.content.move(
    #        source=self,
    #        target=trg['columns'],
    #        safe_id=True)

    def __iter__(self):
        for attr, value in self.__dict__.iteritems():
            yield attr, value

@grok.subscribe(dt_column, IObjectAddedEvent)
def moveObj(column, event):
    container = column.aq_parent
    api.content.move(
        source=column,
        target=container['columns'],
        safe_id=True)
