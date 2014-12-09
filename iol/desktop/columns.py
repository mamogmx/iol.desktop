from five import grok
from AccessControl import ClassSecurityInfo
from plone.dexterity.content import Item
from plone import api
from interfaces import IColumn
from zope.lifecycleevent.interfaces import IObjectAddedEvent
from Products.CMFCore.utils import getToolByName

class dt_column(Item):
    #grok.implements(IColumn)
    #security = ClassSecurityInfo()

    def to_dict(self):
        result = dict(
            mDataProp=self.mDataProp,
            sTitle=self.sTitle,
            sType=self.sType,
            bSortable=str(bool(self.bSortable)).lower(),
            bVisible=str(bool(self.bVisible)).lower()
        )
        if self.sClass:
            result['sClass'] = self.sClass
        if self.sDefaultContent:
            result['sDefaultContent']=self.sDefaultContent
        if self.sWidth:
            result['sWidth']=self.sWidth
        if self.mRender:
            result['mRender']=self.mRender
        return result

@grok.subscribe(dt_column, IObjectAddedEvent)
def moveObj(column, event):
    container = column.aq_parent
    api.content.move(
        source=column,
        target=container['columns'],
        safe_id=True)
