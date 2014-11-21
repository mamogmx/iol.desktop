from zope.interface import Interface

class IDesktopLayer(Interface):
    """Marker interface for the Browserlayer
    """


class IIolProvider(Interface):

    def wfInfo(self):
        """
        @return information about workflow
        """