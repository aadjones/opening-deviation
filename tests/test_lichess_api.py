import pytest
from logic.lichess_api import (
    extract_study_id_from_url,
    get_study_chapters_count,
)

@pytest.mark.parametrize(
    "input_url, expected_output",
    [
        ("https://lichess.org/study/RKEBYTWL/muR4Kgyc", "RKEBYTWL"), 
        ("https://lichess.org/study/bve0Qw48/d7UM1Uru", "bve0Qw48"), 
        ("https://lichess.org/study/RKEBYTWL", "RKEBYTWL")
    ]
)
def test_extract_study_id_from_url_using_chapter(input_url, expected_output):
    assert extract_study_id_from_url(input_url) == expected_output


def test_get_study_chapters_count():
    url = "https://lichess.org/study/bve0Qw48/d7UM1Uru"
    study_id = extract_study_id_from_url(url)
    assert get_study_chapters_count(study_id) == 14
