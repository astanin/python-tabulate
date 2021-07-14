# -*- coding: utf-8 -*-

"""Test output of the various forms of tabular data."""
from tabulate import tabulate
from common import assert_equal


def test_vertical_to_horizontal():
    "Input: a dict of iterables with keys."
    table = {
        "song_name_question": "Toxic",
        "album_name_question": "Singles",
        "artist_name_question": "Britney Spears",
    }

    expected = "\n".join(
        [
            "song_name_question    album_name_question    artist_name_question",
            "Toxic                 Singles                Britney Spears",
        ]
    )

    result = tabulate(table, headers="keys", tablefmt="plain")
    assert_equal(expected, result)
