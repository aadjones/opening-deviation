import pytest
from opening_deviation.opening_deviation import find_deviation, read_pgn, pgn_string_to_game

PGN_PATH = 'pgns/'

def test_find_deviation_1():
    ref_game = read_pgn(PGN_PATH + 'carlsen-nakamura-2020.pgn')
    my_game = read_pgn(PGN_PATH + 'harpseal-rayrey784.pgn')
 
    assert(find_deviation(ref_game, my_game) == (6, 'Qc2', 'Bf4', 'White'))
