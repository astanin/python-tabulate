try:
    from nose.tools import assert_equal
except ImportError:
    def assert_equal(expected, result):
        print("Expected:\n%s\n" % expected)
        print("Got:\n%s\n" % result)
        assert expected == result
