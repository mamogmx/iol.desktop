from Products.CMFPlomino.interfaces import IPlominoDocument

class IDesktopLayer(Interface):
    """Marker interface for the Browserlayer
    """


class IIolAdapter(IPlominoDocument):

    def wfInfo2(self):
        """
        @return information about workflow
        """