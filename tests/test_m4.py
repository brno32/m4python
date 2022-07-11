import pytest

from pathlib import Path

from m4python import mock_p4

from P4 import P4, P4Exception

EXAMPLE_FILE_1 = Path("example.txt")


@mock_p4
def test_m4():
    p4 = P4()  # Create the P4 instance
    p4.port = "1666"
    p4.user = "pytest-user"
    # p4.client should store the name of the client workspace
    p4.client = "P4PyTestWorkspace"  # Set some environment variables

    # test we get the not connected error if we perform an api call before connecting
    with pytest.raises(P4Exception):
        info = p4.run("info")

    p4.connect()

    info = p4.run("info")

    assert info[0]["userName"] == "pytest-user"
    assert info[0]["clientName"] == "P4PyTestWorkspace"
    assert info[0]["clientHost"] == "MockMachine"
    assert info[0]["serverAddress"] == "MockMachine:1666"

    response = p4.run("add", str(EXAMPLE_FILE_1))
    # TODO: check response for sensible values

    change = p4.fetch_change()

    response = p4.run_submit(change)

    response = p4.run("files", "//depot/*")

    assert len(response) == 1

    file_in_depot = response[0]

    assert file_in_depot["depotFile"] == "//depot/example.txt"
    assert file_in_depot["rev"] == "1"
    assert file_in_depot["change"] == "1"
    assert file_in_depot["action"] == "add"
    # TODO: add in check for text and time?
