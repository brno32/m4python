import os
import time

from logging import getLogger
from pathlib import Path

logger = getLogger(__name__)


class VirtualP4:
    """
    A global, in-memory store for all written data when using tests decorated with @mock_p4
    """

    def __init__(self) -> None:
        # properties specific to this library
        self.connected = False

        # values that should be set during connect
        self.username = None
        self.port = 1666
        self.client_name = None

        # hardcoded, mock values
        self.machine_name = "MockMachine"

        # depot stuff - data
        self.depots = {"depot": []}

        self.pending = {"depot": []}

        # depot stuff - metadata
        self.change = "0"

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

    def get_files(self):
        # TODO: dont assume default depot
        # TODO: apply filtering
        return self.depots["depot"]

    def add_file(self, path: Path):
        # TODO: don't assume default depot
        depot_prefix = "//depot"
        path_as_posix = path.as_posix()
        depot_file = f"{depot_prefix}/{path_as_posix}"

        # TODO: don't assume default depot
        for file in self.pending["depot"]:
            if file["depotFile"] == depot_file:
                return [f"{depot_file}#{file['rev']} - currently opened for add"]
        # TODO: don't assume default depot
        for file in self.depots["depot"]:
            if file["depotFile"] == depot_file:
                return [f"{depot_file} - can't add existing file"]

        to_add_to_depo = {
            "depotFile": depot_file,
            "rev": "1",
            "change": "1",
            "action": "add",
            "type": "text",
            "time": f"{int(time.time())}",
        }
        # TODO: don't assume default depot
        self.pending["depot"].append(to_add_to_depo)
        to_return = {**to_add_to_depo}

        # add in or replace values that are different in the return value
        to_return["workRev"] = to_return.pop("rev")
        to_return.pop("time")
        to_return["clientFile"] = os.path.abspath(path)

        return [to_return]

    def fetch_changelist(self):
        return [
            {
                "Change": "new",
                "Client": self.client_name,
                "User": self.username,
                "Status": "new",
                "Description": "<enter description here>\n",
                # TODO: don't assume default depot
                "Files": [file_["depotFile"] for file_ in self.pending["depot"]],
            }
        ]

    def submit_changelist(self):
        # TODO: don't assume default depot
        to_return = []

        # empty pending and reset
        pending = self.pending.pop("depot")
        self.pending["depot"] = []
        self.depots["depot"] += pending

        self.change = f"{int(self.change) + 1}"

        to_return.append(
            {
                "change": self.change,
                # TODO: what is openFiles?
                "openFiles": f"{len(pending)}",
                # TODO: what is locked?
                "locked": f"{len(pending)}",
            }
        )

        for file_ in pending:
            to_return.append(file_)

        to_return.append({"submittedChange": "2"})

        return to_return


virtual_p4 = VirtualP4()
