from unittest.mock import patch

from decorator import decorator

from m4python.m4 import M4

mocked_p4 = patch("P4.P4", M4)
# start the mock outside the decorator so we catch imports before it's applied
mocked_p4.start()


@decorator
def mock_p4(func, *args, **kwargs):
    called = func(*args, **kwargs)
    mocked_p4.stop()
    return called
