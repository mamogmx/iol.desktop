from zope.schema.vocabulary import SimpleVocabulary

map_position = SimpleVocabulary.fromItems([( 'No Map','nomap',), ( 'Position Top','top',),('Position Bottom','bottom',)])

field_type = SimpleVocabulary.fromItems([('search_text', 'Text'), ('search_number', 'Number'),('search_date','Date'),('search_check','Check'),('search_list','List (Dynamic Search)'),])