import pytest  # noqa
from pytest import skip, raises  # noqa
import warnings


def cols_to_pipe_str(cols):
    return "|".join([str(col) for col in cols])


def rows_to_pipe_table_str(rows):
    lines = []
    for row in rows:
        line = cols_to_pipe_str(row)
        lines.append(line)

    return "\n".join(lines)


def check_warnings(func_args_kwargs, *, num=None, category=None, contain=None):
    func, args, kwargs = func_args_kwargs
    with warnings.catch_warnings(record=True) as W:
        # Causes all warnings to always be triggered inside here.
        warnings.simplefilter("always")
        func(*args, **kwargs)
        # Checks
        if num is not None:
            assert len(W) == num
        if category is not None:
            assert all([issubclass(w.category, category) for w in W])
        if contain is not None:
            assert all([contain in str(w.message) for w in W])
