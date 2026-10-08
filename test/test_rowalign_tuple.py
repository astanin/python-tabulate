"""Test for rowalign tuple fix (GitHub issue #440)"""

from tabulate import tabulate


def test_rowalign_tuple_basic():
    """Test that rowalign accepts a tuple without raising TypeError"""
    table = [['Alice', 24], ['Bob', 19]]
    headers = ['Name', 'Age']
    # This used to raise: TypeError: can only concatenate tuple (not "list") to tuple
    result = tabulate(table, headers=headers, rowalign=('center', 'bottom'), tablefmt='grid')
    assert isinstance(result, str)
    assert 'Alice' in result
    assert 'Bob' in result


def test_rowalign_tuple_vs_list_equivalence():
    """Test that tuple and list produce identical output"""
    table = [['Alice', 24], ['Bob', 19], ['Charlie', 30]]
    headers = ['Name', 'Age']
    alignments = ('center', 'bottom', 'top')
    
    result_tuple = tabulate(table, headers=headers, rowalign=alignments, tablefmt='grid')
    result_list = tabulate(table, headers=headers, rowalign=list(alignments), tablefmt='grid')
    
    assert result_tuple == result_list


def test_rowalign_tuple_partial():
    """Test tuple with fewer elements than rows (should pad with default)"""
    table = [['Alice', 24], ['Bob', 19], ['Charlie', 30]]
    headers = ['Name', 'Age']
    # Tuple with only 1 element for 3 rows
    result = tabulate(table, headers=headers, rowalign=('center',), tablefmt='grid')
    assert isinstance(result, str)


def test_rowalign_list_still_works():
    """Ensure list input still works (regression test)"""
    table = [['Alice', 24], ['Bob', 19]]
    headers = ['Name', 'Age']
    result = tabulate(table, headers=headers, rowalign=['center', 'bottom'], tablefmt='grid')
    assert isinstance(result, str)


def test_rowalign_none_still_works():
    """Ensure None input still works (regression test)"""
    table = [['Alice', 24], ['Bob', 19]]
    headers = ['Name', 'Age']
    result = tabulate(table, headers=headers, rowalign=None, tablefmt='grid')
    assert isinstance(result, str)


def test_colalign_tuple():
    """Test that colalign also accepts tuple (uses same _expand_iterable)"""
    table = [['Alice', 24], ['Bob', 19]]
    headers = ['Name', 'Age']
    result = tabulate(table, headers=headers, colalign=('left', 'right'), tablefmt='grid')
    assert isinstance(result, str)


def test_numalign_tuple():
    """Test that numalign also accepts tuple (uses same _expand_iterable)"""
    table = [['Alice', 24], ['Bob', 19]]
    headers = ['Name', 'Age']
    result = tabulate(table, headers=headers, numalign=('right', 'left'), tablefmt='grid')
    assert isinstance(result, str)


def test_stralign_tuple():
    """Test that stralign also accepts tuple (uses same _expand_iterable)"""
    table = [['Alice', 24], ['Bob', 19]]
    headers = ['Name', 'Age']
    result = tabulate(table, headers=headers, stralign=('left', 'right'), tablefmt='grid')
    assert isinstance(result, str)
