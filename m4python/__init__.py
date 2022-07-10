from decorator import decorator


@decorator
def mock_p4(func, *args, **kwargs):
    return func(*args, **kwargs)