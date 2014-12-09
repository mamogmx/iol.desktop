from five import grok
from AccessControl import ClassSecurityInfo
from plone.dexterity.content import IDexterityContent
from plone import api
from interfaces import IColumn
from zope.lifecycleevent.interfaces import IObjectAddedEvent
from Products.CMFCore.utils import getToolByName

class dt_column(IColumn):
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
    container = column.newParent
    api.content.move(
        source=column,
        target=container['columns'],
        safe_id=True)
