import pytest
from logic.chess_utils import (
    find_deviation,
    read_pgn,
    get_player_color,
    find_deviation_in_entire_study)

from logic import lichess_api
from logic.deviation_result import DeviationResult

PGN_PATH = "pgns/"


@pytest.mark.parametrize(
    "ref_pgn_path, my_pgn_path, player, expected",
    [
        (
            "carlsen-nakamura-2020.pgn",
            "harpseal-rayrey784.pgn",
            "HarpSeal",
            DeviationResult(6, "Qc2", "Bf4", "White"),
        ),
        (
            "ref-acc-dragon-1.pgn",
            "acc-dragon-test-1.pgn",
            "Goumas, G.",
            DeviationResult(11, "b6", "a6", "Black"),
        ),
        (
            "ref-acc-dragon-1.pgn",
            "a5-should-be-Re8-jrjrjr4.pgn",
            "Jrjrjr4",
            DeviationResult(8, "a5", "Re8", "Black"),
        ),
        (
            "carlsen-nakamura-2018.pgn",
            "carlsen-nakamura-2018.pgn",
            "Carlsen, M.",
            None,
        ),
        (
            "acc-dragon-test-1.pgn",
            "carlsen-nakamura-2018.pgn",
            "Carlsen, M.",
            None,
        ),
        (
            "acc-dragon-test-1.pgn",
            "opponent-deviates-first.pgn",
            "Jrjrjr4",
            None,
        ),
        (
            "acc-dragon-test-1.pgn",
            "jrjrjr4-last-game-mar-2.pgn",
            "Jrjrjr4",
            DeviationResult(1, "d4", "e4", "White"),
        ),
    ],
)
def test_find_deviation(ref_pgn_path, my_pgn_path, player, expected):
    PGN_PATH = "pgns/"
    ref_game = read_pgn(PGN_PATH + ref_pgn_path)
    my_game = read_pgn(PGN_PATH + my_pgn_path)
    assert find_deviation(ref_game, my_game, player) == expected


@pytest.mark.parametrize(
    "my_pgn_path, player, expected",
    [
        ("harpseal-rayrey784.pgn", "HarpSeal", "White"),
        ("jrjrjr4-last-game.pgn", "Jrjrjr4", "Black"),
    ],
)
def test_get_player_color(my_pgn_path, player, expected):
    PGN_PATH = "pgns/"
    my_game = read_pgn(PGN_PATH + my_pgn_path)
    assert get_player_color(my_game, player) == expected


@pytest.mark.parametrize(
    "ref_study_url, my_pgn_path, player, expected",
    [
        (
            "https://lichess.org/study/bve0Qw48/VgqoWwgW",
            "a5-should-be-Re8-jrjrjr4.pgn",
            "Jrjrjr4",
            DeviationResult(8, "a5", "Re8", "Black"),
        ),
        (
            "https://lichess.org/study/bve0Qw48/VgqoWwgW",
            "played-e6-instead-of-Nd4.pgn",
            "Jrjrjr4",
            DeviationResult(5, "e6", "Nd4", "Black"),
        ),
    ],
)
def test_find_deviation_in_entire_study(
    ref_study_url, my_pgn_path, player, expected
):
    PGN_PATH = "pgns/"
    my_game = read_pgn(PGN_PATH + my_pgn_path)
    assert (
        find_deviation_in_entire_study(
            lichess_api.Study.fetch_url(ref_study_url),
            my_game, player)
        == expected
    )
