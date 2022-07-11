import os

from logging import getLogger

logger = getLogger(__name__)


class VirtualP4:
    """
    A global, in-memory store for all written data when using tests decorated with @mock_p4
    """

    def __init__(self) -> None:
        # values that should be set during connect
        self.username = None
        self.port = 1666
        self.client_name = None

        # hardcoded, mock values
        self.machine_name = "MockMachine"

    def get_info(self):
        return [
            {
                "userName": self.username,
                "clientName": self.client_name,
                "clientCwd": os.getcwd(),
                "clientHost": self.machine_name,
                "clientCase": "insensitive",
                "peerAddress": "127.0.0.1:61532",
                "clientAddress": "127.0.0.1",
                "serverName": "Perforce",
                "serverAddress": f"{self.machine_name}:{self.port}",
                "serverRoot": "C:\\Perforce\\",
                "serverDate": "2022/07/10 17:23:10 -0500 SA Pacific Standard Time",
                "tzoffset": "-18000",
                "serverUptime": "00:02:23",
                "serverVersion": "P4D/NTX64/2022.1/2305383 (2022/06/28)",
                "serverServices": "standard",
                "serverLicense": "none",
                "caseHandling": "insensitive",
                "allowStreamSpecInteg": "1",
                "parentViewDefault": "inheritAll",
                "unloadSupport": "disabled",
                "extensionsSupport": "enabled",
                "memoryManager": "mimalloc 173",
            }
        ]


virtual_p4 = VirtualP4()
