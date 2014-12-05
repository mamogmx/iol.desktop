from five import grok
from AccessControl import ClassSecurityInfo
from z3c.form import group, field
from zope import schema
from zope.interface import invariant, Invalid
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

from plone.dexterity.content import Container,DexterityContent

from plone.directives import dexterity, form
from plone.app.textfield import RichText
from plone.namedfile.field import NamedImage, NamedFile
from plone.namedfile.field import NamedBlobImage, NamedBlobFile
from plone.namedfile.interfaces import IImageScaleTraversable

from z3c.relationfield.schema import RelationList, RelationChoice
from plone.formwidget.contenttree import ObjPathSourceBinder

from plone import api
from iol.desktop import MessageFactory as _
from Products.CMFCore.utils import getToolByName
import simplejson as json
import sqlalchemy as sql
import zope
from Products.CMFCore.CMFBTreeFolder import manage_addCMFBTreeFolder
from interfaces import IMap,IMapLayer

class Google_Map(Container):
    grok.implements(IMap)
    security = ClassSecurityInfo()
    # Add your class methods and properties here
    def __init__(self):
        Container.__init__(self)
        
    def getTemplate(self,id):
        current_path = "/".join(self.getPhysicalPath())
        if id in current_path:
            return current_path[id]
        else:
            template_folder = getToolByName(self, 'portal_skins')
            if 'custom' in template_folder.keys() and id in template_folder['custom'].keys():
                return template_folder['custom'][id]
            else:
                return template_folder['pgdesktop_templates'][id]
            
    def getLayout(self):
        pt = self.getTemplate('mapview')
        map = dict(map = self, layers = self.getLayers())
        return pt.pt_render(extra_context=map)
        
    def getLayers(self):
        result = []
        catalog = getToolByName(self, 'portal_catalog')
        folder_path = '/'.join(self.getPhysicalPath())
        for br in catalog(portal_type='ol_layer',path={'query': folder_path, 'depth': 1}):
            l = br.getObject()
            result.append(l)
        return result
        
      
class olLayer(DexterityContent):
    grok.implements(IMapLayer)
    security = ClassSecurityInfo()
    # Add your class methods and properties here
    
    