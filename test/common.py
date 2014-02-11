try:
    from nose.tools import assert_equal, assert_in


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
