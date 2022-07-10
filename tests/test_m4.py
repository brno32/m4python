from m4python import mock_p4

from P4 import P4, P4Exception  # Import the module


@mock_p4
def test_m4():
    p4 = P4()  # Create the P4 instance
    p4.port = "1666"
    p4.user = "brno32"
    p4.client = "fred-ws"  # Set some environment variables

    p4.connect()
    info = p4.run("info")

    assert info[0]["serverAddress"] == "MachineName:1666"
