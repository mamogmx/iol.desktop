class IolAdapter(object):
    #zope.interface.adapts(IPlominoDocument)

    def __init__(self, context):
        # Each adapter takes the object itself as the construction
        # parameter and possibly provides other parameters for the
        # interface adaption
        self.context = context

    def wfInfo2(self):
        return dict(
            review_state = 'a',
            review_history = []
        )