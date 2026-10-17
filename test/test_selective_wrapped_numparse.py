from tabulate import tabulate


def test_selective_numparse_preserves_wrapped_text_and_numeric_neighbor():
    result = tabulate(
        [["100,120", "1.2300"]],
        headers=["id", "amount"],
        tablefmt="plain",
        maxcolwidths=[4, None],
        disable_numparse=[0],
    )

    assert [line.split() for line in result.splitlines()] == [
        ["id", "amount"],
        ["100,", "1.23"],
        ["120"],
    ]
