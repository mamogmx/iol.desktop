
from zope.interface import Interface

class IDesktopLayer(Interface):
    """Marker interface for the Browserlayer
    """


class IIolAdapter(Interface):

    def wfInfo2(self):
        """
        @return information about workflow
        """