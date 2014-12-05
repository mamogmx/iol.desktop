from five import grok
from AccessControl import ClassSecurityInfo
from z3c.form import group, field
from zope import schema
from zope.interface import invariant, Invalid
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

from plone.dexterity.content import Container

from plone.directives import dexterity, form
from plone.app.textfield import RichText
from plone.namedfile.field import NamedImage, NamedFile
from plone.namedfile.field import NamedBlobImage, NamedBlobFile
from plone.namedfile.interfaces import IImageScaleTraversable

from plone.formwidget.contenttree import ObjPathSourceBinder

from plone import api
from iol.desktop import MessageFactory as _
from Products.CMFCore.utils import getToolByName
import simplejson as json
import sqlalchemy as sql
import zope
from Products.CMFCore.CMFBTreeFolder import manage_addCMFBTreeFolder
from zope.interface import Interface

class IDesktopLayer(Interface):
    """Marker interface for the Browserlayer
    """
class IMap(form.Schema):
    """"Marker Interface for Imap
    """
    form.model("models/google_map.xml")

class IMapLayer(Interfaces):
    """Marker Interfaces for IMapLayer
    """
