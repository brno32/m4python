from m4python.virtual import virtual_p4


class M4Adapter:
    @staticmethod
    def connect(p4):
        pass


class M4API:
    """
    Overrides the P4API class which acts as the interface to the C++ API (and consequently a Perforce server)
    and instead redirects requests to the globally instantiated VirtualP4 instance (virtual_p4 from m4python.virtual)
    """

    P4Adapter = M4Adapter
