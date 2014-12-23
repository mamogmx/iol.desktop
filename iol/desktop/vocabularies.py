from five import grok
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary
from Products.CMFCore.utils import getToolByName

class listGroups(object):
    grok.implements(IContextSourceBinder)
    def __call__(self,context):
        acl_users = getToolByName(context, 'acl_users')
        group_list = acl_users.source_groups.getGroups()
        terms = [SimpleVocabulary.createTerm('AuthenticatedUsers', 'AuthenticatedUsers', 'Authenticated Users')]
        for group in group_list:
            terms.append(SimpleVocabulary.createTerm(group.getName(), group.getName() ,group.title or  group.getName()))
        return SimpleVocabulary(terms)

class listMaps(object):
    grok.implements(IContextSourceBinder)
    def __call__(self,context):
        folder_path = '/'.join(context.getPhysicalPath())
        catalog = getToolByName(context, 'portal_catalog')
        terms = list()
        for br in catalog(portal_type='google_map',path={'query': folder_path, 'depth': 2}):
            map = br.getObject()
            terms.append(SimpleVocabulary.createTerm(map.id, map.id ,map.title or  map.id))
        
        return SimpleVocabulary(terms)

class listFields(object):
    grok.implements(IContextSourceBinder)
    def __call__(self,context):
        terms = list()
        desktop = context
        conn = desktop.getConn()
        query = "select distinct json_object_keys(data) as columns from %s.%s order by 1" %(desktop.db_schema,desktop.db_table)
        for r in conn.execute(query):
            terms.append(SimpleVocabulary.createTerm(r['columns'],r['columns'],r['columns']))
        return SimpleVocabulary(terms)
        
map_position = SimpleVocabulary.fromItems([( 'No Map','nomap',), ( 'Position Top','top',),('Position Bottom','bottom',)])
map_list = listMaps()

field_type = SimpleVocabulary.fromItems([( 'Text', 'search_text',), ('Number', 'search_number', ),('Date','search_date',),('Check','search_check',),('Radio','search_radio',),('List (Dynamic Search)','search_list',),])
field_list = listFields()
yes_no = SimpleVocabulary.fromItems([('Yes',1),('No',0)])
view_type = SimpleVocabulary.fromItems([('Text','text'),('Integer','integer'),('Float','float'),('Date','date')])
users_groups_list = listGroups()