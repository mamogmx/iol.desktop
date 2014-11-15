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

from plone import api
from iol.desktop import MessageFactory as _
from Products.CMFCore.utils import getToolByName
import simplejson as json
import sqlalchemy as sql
import zope

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
    @zope.interface.invariant
    def isValidConnectionString(desktop):
        try:
            engine = sql.create_engine(desktop.conn_string)
            connection = engine.connect()
        except:
            raise zope.interface.Invalid("Not a valid connection string '%s'" %desktop.conn_string)

# Custom content-type class; objects created for this content type will
# be instances of this class. Use this class to add content-type specific
# methods and properties. Put methods that are mainly useful for rendering
# in separate view classes.

class pg_desktop(Container):
    grok.implements(Ipg_desktop)

    # Add your class methods and properties here
    def getFields(self):
        results = []
        portal_catalog = api.portal.get_tool(name='portal_catalog')
        current_path = "/".join(self.context.getPhysicalPath())

        brains = portal_catalog(portal_type="pg_search_field",
                                path=current_path)
        for brain in brains:
            i = brain.getObject()
            try:
                v = json.loads(i.search_val)
            except:
                v = list()
            try:
                opt = json.loads(i.search_opt)
            except:
                opt = dict()
            if i.subfield_name:
                name = "%s-->'%s'" %(i.field_name,i.subfield_name )
            else:
                name = i.field_name
                
            obj = dict(name=name,title=i.title,values=v,option=opt,template=i.fieldtype)
            results.append(obj)
        return results
        
    def getTemplate(self,id):
        current_path = "/".join(self.context.getPhysicalPath())
        template_id = ''
#       current_path
        if id in current_path:
            return current_path[id]
        else:
            template_folder =  api.portal.get_tool(name = 'pg_desktop_template')
            return  template_folder[id]

    def displayLayout(self):
        fields = self.getFields()
        html_content = self.page.getRaw()
        for field in fields:
            fieldblock = '<span class="desktopField">%s</span>' %field.name
            pt = self.getTemplate(field.template)
            html = pt.pt_render(extra_content = field)
            html_content.replace(fieldblock,html)
        return html_content
        
    def pgSearch(self):
        request = self.REQUEST
        result = {'aaData': list(), 'sEcho': request.get('sEcho',0), 'iTotalRecords': 0, 'iTotalDisplayRecords': 0, 'error':''}
        engine = sql.create_engine(self.conn_string)
        connection = engine.connect()
        tb = self.db_table
        sk = self.db_schema
        dt = pgDataTables(sk,tb,request)
        queryTot = dt.findTotal()
        query = dt.findResult()

        resTot = connection.execute(queryTot)
        totali = int(resTot.fetchall()[0]["totali"])
        result["iTotalRecords"] = totali

        res = connection.execute(query)
        for r in res:
            data = json.loads(r)
            data[id] = r["id"]
            result['aaData'].append(data)
        result['iTotalDisplayRecords'] = len(result['aaData'])
        request.RESPONSE.headers['Content-Type'] = 'application/json'
        return result
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
