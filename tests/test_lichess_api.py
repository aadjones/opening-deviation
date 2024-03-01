from logic.lichess_api import extract_study_id_from_url
from logic.deviation_result import DeviationResult

def test_extract_study_id_from_url_base():
    url = 'https://lichess.org/study/RKEBYTWL'
    assert(extract_study_id_from_url(url) == 'RKEBYTWL')

def test_extract_study_id_from_url_using_chapter():
    url = 'https://lichess.org/study/RKEBYTWL/muR4Kgyc'
    assert(extract_study_id_from_url(url) == 'RKEBYTWL')
