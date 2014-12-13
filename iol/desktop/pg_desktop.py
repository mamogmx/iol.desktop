from five import grok
from AccessControl import ClassSecurityInfo

from plone.dexterity.content import Container

import re
from plone import api
from plone.directives import dexterity, form
from iol.desktop import MessageFactory as _
from Products.CMFCore.utils import getToolByName
import simplejson as json
import sqlalchemy as sql
import zope
from Products.CMFCore.CMFBTreeFolder import manage_addCMFBTreeFolder


# Interface class; used to define content-type schema.


class Ipg_desktop(form.Schema):
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
    security = ClassSecurityInfo()
    # Add your class methods and properties here

    def __init__(self):
        Container.__init__(self)
        manage_addCMFBTreeFolder(self, id='resources')
        self.invokeFactory('Folder', id='columns')
        #manage_addCMFBTreeFolder(self, id='columns')
        #api.content.create(container=self, type='Folder', id='columns')

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
                    (val, lbl) = l.split('|')
                    v.append(dict(label=lbl, value=val))
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

    def getDTColumns(self):
        results = []

        if self['columns'].keys():
            for i in self['columns'].items():
                cols = i[1].to_dict()
                results.append(cols)
        else:
            from zope.globalrequest import getRequest
            request = getRequest()
            api.portal.show_message("No Datatables Columns defined.Please add some DT Columns",request,'warn')
            request.RESPONSE.redirect("%s/++add++dt_column" % self.absolute_url())
        return results
            
    def getTemplate(self,id):
        current_path = "/".join(self.getPhysicalPath())
        if id in current_path:
            return current_path[id]
        else:
            template_folder = getToolByName(self, 'portal_skins')
            template_folder = template_folder['pgdesktop_templates']
            return template_folder[id]
            
    def getMap(self):
        if self.desktop_with_map != 'nomap' and self.map_name:
            portal_catalog = api.portal.get_tool(name='portal_catalog')
            current_path = "/".join(self.getPhysicalPath())
            brains = portal_catalog(portal_type="google_map",id = self.map_name, path=current_path)
            
            map = brains[0].getObject()
        else:
            map = None
        return map

    def displayLayout(self):

        fields = self.getFields()
        cols = self.getDTColumns()

        html_content = self.html_slot.raw

        for fld in fields:
            fieldblock = '<span class="desktopField">%s</span>' % fld['name']
            pt = self.getTemplate(fld['template'])
            html = pt.pt_render(extra_context=fld)
            html_content = html_content.replace(fieldblock, html)

        dtblock = '<span class="desktopTable">Result Table</span>'
        pt = self.getTemplate('resultTable')
        columns = json.dumps(cols)
        m = re.findall('"mRender": "([A-z0-9_]+)"', columns)
        for r in m:
            columns.replace('"mRender": "%s"' % r,'"mRender": %s' % r)
        html = pt.pt_render(extra_context=dict(cols=columns))
        html_content = html_content.replace(dtblock, html)

        if self.desktop_with_map != 'nomap' and self.map_name:
            mapblock = '<span class="desktopMap">%s</span>' % self.map_name
            html = self.getMap().displayLayout()
            html_content = html_content.replace(mapblock, html)

        return html_content
        
    def getConn(self):
        engine = sql.create_engine(self.conn_string)
        connection = engine.connect()
        return connection

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