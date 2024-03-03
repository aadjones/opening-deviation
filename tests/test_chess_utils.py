from logic.chess_utils import (
    find_deviation,
    read_pgn,
    get_player_color,
    find_deviation_in_entire_study,
)
from logic.deviation_result import DeviationResult

PGN_PATH = "pgns/"


def test_find_deviation_white():
    ref_game = read_pgn(PGN_PATH + "carlsen-nakamura-2020.pgn")
    my_game = read_pgn(PGN_PATH + "harpseal-rayrey784.pgn")

    assert find_deviation(ref_game, my_game, "HarpSeal") == DeviationResult(
        6, "Qc2", "Bf4", "White"
    )


def test_find_deviation_black():
    ref_game = read_pgn(PGN_PATH + "ref-acc-dragon-1.pgn")
    my_game = read_pgn(PGN_PATH + "acc-dragon-test-1.pgn")

    assert find_deviation(ref_game, my_game, "Goumas, G.") == DeviationResult(
        11, "b6", "a6", "Black"
    )


def test_find_deviation_black_a5():
    ref_game = read_pgn(PGN_PATH + "ref-acc-dragon-1.pgn")
    my_game = read_pgn(PGN_PATH + "a5-should-be-Re8-jrjrjr4.pgn")

    assert find_deviation(ref_game, my_game, "Jrjrjr4") == DeviationResult(
        8, "a5", "Re8", "Black"
    )


def test_find_deviation_when_equal():
    ref_game = read_pgn(PGN_PATH + "carlsen-nakamura-2018.pgn")

    assert find_deviation(ref_game, ref_game, "Carlsen, M.") is None


def test_find_deviation_when_wrong_color():
    ref_game = read_pgn(PGN_PATH + "acc-dragon-test-1.pgn")
    my_game = read_pgn(PGN_PATH + "carlsen-nakamura-2018.pgn")

    assert find_deviation(ref_game, my_game, "Carlsen, M.") is None


def test_opponent_deviates_first():
    ref_game = read_pgn(PGN_PATH + "acc-dragon-test-1.pgn")
    my_game = read_pgn(PGN_PATH + "opponent-deviates-first.pgn")

    assert find_deviation(ref_game, my_game, "Jrjrjr4") is None


def test_wrong_color_test_2():
    ref_game = read_pgn(PGN_PATH + "acc-dragon-test-1.pgn")
    my_game = read_pgn(PGN_PATH + "jrjrjr4-last-game-mar-2.pgn")

    assert find_deviation(ref_game, my_game, "Jrjrjr4") == DeviationResult(
        1, "d4", "e4", "White"
    )


def test_get_player_color_white():
    my_game = read_pgn(PGN_PATH + "harpseal-rayrey784.pgn")

    assert get_player_color(my_game, "HarpSeal") == "White"


def test_get_player_color_black():
    my_game = read_pgn(PGN_PATH + "jrjrjr4-last-game.pgn")

    assert get_player_color(my_game, "Jrjrjr4") == "Black"


def test_find_deviation_in_entire_study_ch_1():
    ref_study_url = "https://lichess.org/study/bve0Qw48/VgqoWwgW"
    my_game = read_pgn(PGN_PATH + "a5-should-be-Re8-jrjrjr4.pgn")

    assert find_deviation_in_entire_study(
        ref_study_url, my_game, "Jrjrjr4"
    ) == DeviationResult(8, "a5", "Re8", "Black")


def test_find_deviation_in_entire_study_later_chapter():
    ref_study_url = "https://lichess.org/study/bve0Qw48/VgqoWwgW"
    my_game = read_pgn(PGN_PATH + "played-e6-instead-of-Nd4.pgn")

    assert find_deviation_in_entire_study(
        ref_study_url, my_game, "Jrjrjr4"
    ) == DeviationResult(5, "e6", "Nd4", "Black")
