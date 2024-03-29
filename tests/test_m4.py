import os
import pytest

from pathlib import Path

from m4python import mock_p4

from P4 import P4, P4Exception

TESTS_DIR = Path("tests")

EXAMPLE_FILE_1 = TESTS_DIR / "example1.txt"


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

    response = p4.run("add", EXAMPLE_FILE_1)
    assert response[0]["depotFile"] == f"//depot/{EXAMPLE_FILE_1.as_posix()}"
    assert response[0]["clientFile"] == str(Path(os.getcwd()) / EXAMPLE_FILE_1)
    assert response[0]["workRev"] == "1"
    assert response[0]["action"] == "add"
    assert response[0]["type"] == "text"

    # now test that if we try to add the same file again once it's already pending, we get the currently opened for add message
    response = p4.run("add", EXAMPLE_FILE_1)
    assert (
        response[0]
        == f"//depot/{EXAMPLE_FILE_1.as_posix()}#1 - currently opened for add"
    )

    change = p4.fetch_change()

    change._description = "Changelist from python"

    response = p4.run_submit(change)

    response = p4.run("files", "//depot/*")

    assert len(response) == 1

    file_in_depot = response[0]

    assert file_in_depot["depotFile"] == f"//depot/{EXAMPLE_FILE_1.as_posix()}"
    assert file_in_depot["rev"] == "1"
    assert file_in_depot["change"] == "1"
    assert file_in_depot["action"] == "add"
    # TODO: add in check for text and time?

    # now check that we can't add the same files again
    response = p4.run("add", EXAMPLE_FILE_1)
    assert (
        response[0] == f"//depot/{EXAMPLE_FILE_1.as_posix()} - can't add existing file"
    )

    # now see if we can edit that file
    response = p4.run("edit", EXAMPLE_FILE_1)
    assert response[0]["depotFile"] == f"//depot/{EXAMPLE_FILE_1.as_posix()}"
    assert response[0]["action"] == "edit"
    assert response[0]["workRev"] == "2"
    assert response[0]["clientFile"] == str(Path(os.getcwd()) / EXAMPLE_FILE_1)

    # make sure we can't edit twice
    response = p4.run("edit", EXAMPLE_FILE_1)
    assert (
        response[0]
        == f"//depot/{EXAMPLE_FILE_1.as_posix()}#2 - currently opened for edit"
    )

    # and check we can't edit a non-existent file
    with pytest.raises(P4Exception):
        p4.run("edit", "awef" / EXAMPLE_FILE_1)

    change = p4.fetch_change()

    change._description = "Changelist from python"

    response = p4.run_submit(change)

    response = p4.run("files", "//depot/*")

    assert len(response) == 1

    file_in_depot = response[0]
    assert file_in_depot["depotFile"] == f"//depot/{EXAMPLE_FILE_1.as_posix()}"
    assert file_in_depot["rev"] == "2"
    assert file_in_depot["change"] == "2"
    assert file_in_depot["action"] == "edit"
