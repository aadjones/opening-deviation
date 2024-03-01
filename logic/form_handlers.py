"""
This module provides the logic for the user input/output on the website through streamlit.
"""

from typing import Optional
import streamlit as st
from .lichess_api import get_pgn_from_study, get_last_games_pgn
from .chess_utils import pgn_string_to_game, find_deviation
from .deviation_result import DeviationResult


def handle_form_submission(username: str, study_url: str, chapter_number: str) -> None:
    """
    Handles form submission and displays the result.

    :param username: str, the Lichess username
    :param study_url: str, the URL of the Lichess study
    :param chapter_number: str, the chapter number of the Lichess study
    :return: None
    """
    chapter = int(chapter_number)

    # Get the PGN data from the Lichess study
    ref_pgn_str = get_pgn_from_study(study_url, chapter)

    # Fetch the last game played by the user
    max_games = 1
    test_game_str = get_last_games_pgn(username, max_games)

    # Convert PGN strings to game objects
    test_game = pgn_string_to_game(test_game_str)
    reference_game = pgn_string_to_game(ref_pgn_str)

    # Find deviation between games
    deviation_info = find_deviation(reference_game, test_game)

    display_deviation_info(deviation_info)


def display_deviation_info(deviation_info: Optional[DeviationResult]) -> None:
    """
    Displays the deviation information.

    :param deviation_info: DeviationResult or None, information about the deviation
    :return: None
    """
    if deviation_info:
        i = deviation_info.whole_move_number
        dev_move = deviation_info.deviation_san
        ref_move = deviation_info.reference_san
        color = deviation_info.player_color
        # For example, move 2 will be 2. if White or 2... if Black
        periods = '.' if color == 'White' else '...'
        dev_move_notation = f'{i}{periods}{dev_move}'
        ref_move_notation = f'{i}{periods}{ref_move}'
        st.write(f'Deviating move: {dev_move_notation}')
        st.write(f'Reference move: {ref_move_notation}')
    else:
        st.write('No deviation found in the last game played.')
