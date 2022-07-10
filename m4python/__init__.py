from unittest.mock import patch

from decorator import decorator

from m4python.m4api import M4API

mocked_p4 = patch("P4.P4API", M4API)
# start the mock outside the decorator so we catch imports before it's applied
mocked_p4.start()


@decorator
def mock_p4(func, *args, **kwargs):
    called = func(*args, **kwargs)
    mocked_p4.stop()
    return called
