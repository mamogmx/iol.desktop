from five import grok
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary
from Products.CMFCore.utils import getToolByName

class listGroups(object):
    grok.implements(IContextSourceBinder)
    def __call__(self,context):
        acl_users = getToolByName(context, 'acl_users')
        group_list = acl_users.source_groups.getGroups()
        terms = [SimpleVocabulary.createTerm('Authenticated Users', 'Authenticated Users', 'Authenticated Users')]
        for group in group_list:
            terms.append(SimpleVocabulary.createTerm(group.getName(), group.getName() ,group.title or  group.getName()))
        return SimpleVocabulary(terms)

map_position = SimpleVocabulary.fromItems([( 'No Map','nomap',), ( 'Position Top','top',),('Position Bottom','bottom',)])

field_type = SimpleVocabulary.fromItems([( 'Text', 'search_text',), ('Number', 'search_number', ),('Date','search_date',),('Check','search_check',),('List (Dynamic Search)','search_list',),])

users_groups_list = listGroups()