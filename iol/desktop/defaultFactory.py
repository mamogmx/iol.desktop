from five import grok
from zope.schema.interfaces import IContextAwareDefaultFactory

@grok.provider(IContextAwareDefaultFactory)
def dtorder(context):
    return 2