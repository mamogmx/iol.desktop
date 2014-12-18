from five import grok
from zope.schema.interfaces import IContextAwareDefaultFactory
from Products.CMFCore.utils import getToolByName

@grok.provider(IContextAwareDefaultFactory)
def dtorder(context):
    catalog = getToolByName(context, 'portal_catalog')
    folder_path = '/'.join(context.getPhysicalPath())
    max = 0
    for br in catalog(portal_type='dt_column',path={'query': folder_path, 'depth': 2}):
        col = br.getObject()
        if col.order > max:
            max = col.order
    return max + 1