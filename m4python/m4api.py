from P4 import P4Exception

from m4python.virtual import virtual_p4


class M4Adapter:
    @staticmethod
    def connect(p4):
        virtual_p4.connected = True
        # TODO: pass some mock info to the p4 instance?
        virtual_p4.username = p4.user
        virtual_p4.port = p4.port
        virtual_p4.client_name = p4.client

    @staticmethod
    def run(p4, *args):
        if not virtual_p4.connected:
            raise P4Exception("[P4.run()] not connected.")

        if args[0] == "info":
            return virtual_p4.get_info()
        elif args[0] == "files":
            return virtual_p4.get_files()
        elif args[0] == "add":
            return virtual_p4.add_file(args[1])
        elif args[0] == "change":
            return virtual_p4.fetch_changelist()
        elif args[0] == "submit":
            return virtual_p4.submit_changelist()


class M4API:
    """
    Overrides the P4API class which acts as the interface to the C++ API (and consequently a Perforce server)
    and instead redirects requests to the globally instantiated VirtualP4 instance (virtual_p4 from m4python.virtual)
    """

    P4Adapter = M4Adapter
