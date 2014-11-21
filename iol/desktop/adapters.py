import zope.interface
from Products.CMFPlomino.interfaces import IPlominoDocument,IPlominoForm

class IolAdapters(object):

    zope.interface.implements(IPlominoDocument)
    zope.interface.implements(IPlominoForm)

    def __init__(self, context):
        # Each adapter takes the object itself as the construction
        # parameter and possibly provides other parameters for the
        # interface adaption
        self.context = context

    def wfInfo(self):
        return dict(
            review_state = 'a',
            review_history = []
        )