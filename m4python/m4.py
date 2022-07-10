from P4 import P4

from m4python.virtual import virtual_p4


class M4(P4):
    """
    Overrides methods from the P4 class which call the C++ API (and consequently a Perforce server) and instead
    redirects requests to the virtual Perforce server
    """

    def connect(self):
        return self

    def run(self, *args, **kargs):
        if args[0] == "info":
            return virtual_p4.info
        return super().run(*args, **kargs)
