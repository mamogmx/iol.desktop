from zope.schema.vocabulary import SimpleVocabulary
from plone import api

def listGroups():
    return SimpleVocabulary.fromItems([(grp.title,grp.groupname) for grp in api.group.get_groups()])

map_position = SimpleVocabulary.fromItems([( 'No Map','nomap',), ( 'Position Top','top',),('Position Bottom','bottom',)])

field_type = SimpleVocabulary.fromItems([( 'Text', 'search_text',), ('Number', 'search_number', ),('Date','search_date',),('Check','search_check',),('List (Dynamic Search)','search_list',),])

users_groups_list = listGroups()