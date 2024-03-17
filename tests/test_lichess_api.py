import pytest
from logic.lichess_api import _extract_study_id_from_url


@pytest.mark.parametrize(
    "input_url, expected_output",
    [
        ("https://lichess.org/study/RKEBYTWL/muR4Kgyc", "RKEBYTWL"),
        ("https://lichess.org/study/bve0Qw48/d7UM1Uru", "bve0Qw48"),
        ("https://lichess.org/study/RKEBYTWL", "RKEBYTWL"),
    ],
)
def test_extract_study_id_from_url_using_chapter(input_url, expected_output):
    assert _extract_study_id_from_url(input_url) == expected_output
