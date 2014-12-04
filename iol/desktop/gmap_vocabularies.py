from five import grok
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary
from Products.CMFCore.utils import getToolByName

map_type = SimpleVocabulary.fromItems([( 'Hybrid', 'HYBRID',), ('RoadMap', 'ROADMAP', ),('Satellite','SATELLITE',),('Terrain','TERRAIN',),])