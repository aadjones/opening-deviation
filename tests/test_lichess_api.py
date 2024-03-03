from logic.lichess_api import extract_study_id_from_url, get_study_chapters_count

def test_extract_study_id_from_url_base():
    url = 'https://lichess.org/study/RKEBYTWL'
    assert extract_study_id_from_url(url) == 'RKEBYTWL'

def test_extract_study_id_from_url_using_chapter():
    url = 'https://lichess.org/study/RKEBYTWL/muR4Kgyc'
    assert extract_study_id_from_url(url) == 'RKEBYTWL'

def test_extract_study_id_from_url_using_chapter_2():
    url = 'https://lichess.org/study/bve0Qw48/d7UM1Uru'  
    assert extract_study_id_from_url(url) == 'bve0Qw48'


def test_get_study_chapters_count():
    url = 'https://lichess.org/study/bve0Qw48/d7UM1Uru'
    study_id = extract_study_id_from_url(url)
    assert get_study_chapters_count(study_id) == 14
