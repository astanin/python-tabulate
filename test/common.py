try:
    from nose.tools import assert_equal, assert_in, assert_raises


except ImportError:
    def assert_equal(expected, result):
        print("Expected:\n%s\n" % expected)
        print("Got:\n%s\n" % result)
        assert expected == result


    def assert_in(result, expected_set):
        nums = xrange(1, len(expected_set)+1)
        for i, expected in zip(nums, expected_set):
            print("Expected %d:\n%s\n" % (i, expected))
        print("Got:\n%s\n" % result)
        assert result in expected_set


    class assert_raises(object):
        def __init__(self, exception_type):
            self.watch_exception_type = exception_type
        def __enter__(self):
            pass
        def __exit__(self, exception_type, exception_value, traceback):
            if isinstance(exception_value, self.watch_exception_type):
                return True  # suppress exception
            elif exception_type is None:
                msg = "%s not raised" % self.watch_exception_type.__name__
                raise AssertionError(msg)
            # otherwise propagate whatever other exception is raised
