from unittest.mock import patch

from decorator import decorator

from m4python.m4 import M4


@decorator
def mock_p4(func, *args, **kwargs):
    mocked_p4 = patch("P4.P4", M4)
    mocked_p4.start()
    called = func(*args, **kwargs)
    mocked_p4.stop()
    return called
