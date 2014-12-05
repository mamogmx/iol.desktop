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


class olLayer(DexterityContent):
    grok.implements(IMapLayer)
