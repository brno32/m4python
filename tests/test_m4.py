import pytest

from m4python import mock_p4

from P4 import P4, P4Exception


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
    print(info)

    assert info[0]["serverAddress"] == "MockMachine:1666"
