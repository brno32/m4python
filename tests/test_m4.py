from m4python import mock_p4


@mock_p4
def test_m4():
    from P4 import P4, P4Exception  # Import the module

    p4 = P4()  # Create the P4 instance
    p4.port = "1666"
    p4.user = "fred"
    p4.client = "fred-ws"  # Set some environment variables

    try:  # Catch exceptions with try/except
        p4.connect()  # Connect to the Perforce server
    except P4Exception as reason:
        print(reason)
        assert False
