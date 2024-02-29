from opening_deviation.opening_deviation import find_deviation, read_pgn, pgn_string_to_game
from opening_deviation.opening_deviation import extract_study_id_from_url

PGN_PATH = 'pgns/'

def test_find_deviation_1():
    ref_game = read_pgn(PGN_PATH + 'carlsen-nakamura-2020.pgn')
    my_game = read_pgn(PGN_PATH + 'harpseal-rayrey784.pgn')
 
    assert(find_deviation(ref_game, my_game) == (6, 'Qc2', 'Bf4', 'White'))

def test_find_deviation_when_equal():
    ref_game = read_pgn(PGN_PATH + 'carlsen-nakamura-2018.pgn')

    assert(find_deviation(ref_game, ref_game) == None)

def test_extract_study_id_from_url_1():
    url = 'https://lichess.org/study/RKEBYTWL/muR4Kgyc'
    assert(extract_study_id_from_url(url) == 'RKEBYTWL')
