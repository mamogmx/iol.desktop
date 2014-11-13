from five import grok

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

from z3c.relationfield.schema import RelationList, RelationChoice
from plone.formwidget.contenttree import ObjPathSourceBinder


from iol.desktop import MessageFactory as _
from Products.CMFCore.utils import getToolByName
import simplejson as json

# Interface class; used to define content-type schema.

class Ipg_desktop(form.Schema, IImageScaleTraversable):
    """
    Desktop for IOL Application connected with Postgres Database
    """

    # If you want a schema-defined interface, delete the model.load
    # line below and delete the matching file in the models sub-directory.
    # If you want a model-based interface, edit
    # models/pg_desktop.xml to define the content type.

    form.model("models/pg_desktop.xml")


# Custom content-type class; objects created for this content type will
# be instances of this class. Use this class to add content-type specific
# methods and properties. Put methods that are mainly useful for rendering
# in separate view classes.

class pg_desktop(Container):
    grok.implements(Ipg_desktop)

    # Add your class methods and properties here
    def getFields(self):
        results = []
        portal_catalog = getToolByName(self.context, 'portal_catalog')
        current_path = "/".join(self.context.getPhysicalPath())

        brains = portal_catalog(portal_type="pg_searcg_field",
                                path=current_path)
        for brain in brains:
            i = brain.getObject()
            v = list()
            opt = dict()
            obj = dict(name=i.id,title=i.title,values=v,option=opt,template=i.fieldType)
            results.append(obj)
        return results
        
    def getTemplate(self,id):
        portal_catalog = getToolByName(self.context, 'portal_catalog')
        current_path = "/".join(self.context.getPhysicalPath())
        brains = portal_catalog(id = id,portal_type="",path=current_path)
        if len(brains)>0:
            return brains[0].getObject()
        else:
            template_folder =  getToolByName(self.context, 'pg_desktop_template')
            brains = portal_catalog(id = id,portal_type="",path="/".join(template_folder.getPhysicalPath()))
            return brains[0].getObject()
            
    def displayLayout(self):
        fields = self.getFields()
        html_content = self.page.getRaw()
        for field in fields:
            fieldblock = '<span class="desktopField">%s</span>' %field.name
            pt = self.getTemplate(field.template)
            html = pt( )
            html_content.replace(fieldblock,html)
        return html_content
        
    def pgSearch(self):
        
        pass


# View class
# The view will automatically use a similarly named template in
# pg_desktop_templates.
# Template filenames should be all lower case.
# The view will render when you request a content object with this
# interface with "/@@sampleview" appended.
# You may make this the default view for content objects
# of this type by uncommenting the grok.name line below or by
# changing the view class name and template filename to View / view.pt.

class View(grok.View):
    """ sample view class """

    grok.context(Ipg_desktop)
    grok.require('zope2.View')
    
    grok.name('view')

    # Add view methods here
