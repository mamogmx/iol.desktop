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

from z3c.relationfield.schema import RelationList, RelationChoice
from plone.formwidget.contenttree import ObjPathSourceBinder

from plone import api
from iol.desktop import MessageFactory as _
from Products.CMFCore.utils import getToolByName
import simplejson as json
import sqlalchemy as sql
import zope
from Products.CMFCore.CMFBTreeFolder import manage_addCMFBTreeFolder

from iol.desktop.datatables import pgDataTables

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
    #@zope.interface.invariant
    #def isValidConnectionString(desktop):
    #    try:
    #        engine = sql.create_engine(desktop.conn_string)
    #        connection = engine.connect()
    #    except:
    #        pass
    #        raise zope.interface.Invalid("Not a valid connection string '%s'" %desktop.conn_string)

# Custom content-type class; objects created for this content type will
# be instances of this class. Use this class to add content-type specific
# methods and properties. Put methods that are mainly useful for rendering
# in separate view classes.

class pg_desktop(Container):
    grok.implements(Ipg_desktop)
    security = ClassSecurityInfo()
    # Add your class methods and properties here
    def __init__(self):
        Container.__init__(self)
        manage_addCMFBTreeFolder(self, id='resources')

    def getFields(self):
        results = []
        portal_catalog = api.portal.get_tool(name='portal_catalog')
        current_path = "/".join(self.getPhysicalPath())

        brains = portal_catalog(portal_type="pg_search_field",
                                path=current_path)
        for brain in brains:
            i = brain.getObject()
            try:
                v = list()
                lst = i.search_val.split(',')
                for l in lst:
                    (val,lbl) = l.split('|')
                    v.append(dict(label=lbl,value=val))
            except Exception as e:
                
                print str(e)
                v = [{'value':'error','label':'Errore'}]
            try:
                opt = json.loads(i.search_opt)
            except:
                opt = dict()

                
            obj = dict(
                name=i.id,
                title=i.title,
                values=v,
                option=opt,
                template=i.field_type,
                fieldname=i.field_name,
                subfieldname=i.subfield_name
            )
            results.append(obj)
        return results
       
    def loadResources(self):
        result = dict(
            css = ['/++resource++iol.desktop/bootstrap.css','/++resource++iol.desktop/bootstrap-responsive.css','/++resource++iol.desktop/bootstrap.dataTables.css','/++resource++iol.desktop/desktop.css'],
            js = ['/++resource++iol.desktop/bootstrap.min.js','/++resource++iol.desktop/bootstrap.dataTables.js','/++resource++iol.desktop/search.pgdesktop.js']
        )
        if 'resources' in self.keys():
            res = self['resources']
            for f in res.keys():
                if f.endswith('.css'):
                    result['css'].append('resources/%s' %f)
                elif f.endswith('.js'):
                    result['js'].append('resources/%s' %f)
        return result
            
    def getTemplate(self,id):
        current_path = "/".join(self.getPhysicalPath())
        if id in current_path:
            return current_path[id]
        else:
            template_folder = getToolByName(self, 'portal_skins')
            template_folder = template_folder['pgdesktop_templates']
            return template_folder[id]

    def displayLayout(self, layout):
        def top_layout(obj):
            if obj.top_slot:
                return obj.top_slot.raw
            else:
                return ''

        def bottom_layout(obj):
            if obj.bottom_slot:
                return obj.bottom_slot.raw
            else:
                return ''

        def left_layout(obj):
            if obj.left_slot:
                return obj.left_slot.raw
            else:
                return ''

        def right_layout(obj):
            if obj.right_slot:
                return obj.right_slot.raw
            else:
                return ''

        option = {
            'top_slot': top_layout,
            'left_slot': left_layout,
            'bottom_slot': bottom_layout,
            'right_slot': right_layout
        }
        fields = self.getFields()
        if not layout in ('top_slot', 'bottom_slot', 'left_slot', 'right_slot'):
            return ''
        html_content = option[layout](self)
        if not html_content:
            return ''
        for fld in fields:
            fieldblock = '<span class="desktopField">%s</span>' % fld['name']
            pt = self.getTemplate(fld['template'])
            html = pt.pt_render(extra_context=fld)
            html_content = html_content.replace(fieldblock, html)
        return html_content

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