"""
This module provides the logic for the user input/output on the website through streamlit.
"""

from typing import Optional
import streamlit as st
from .lichess_api import get_pgn_from_study, get_last_games_pgn
from .chess_utils import pgn_string_to_game, find_deviation, find_deviation_in_entire_study, pgn_to_pgn_list
from .deviation_result import DeviationResult


def handle_form_submission(username: str, study_url: str, max_games: int) -> None:
    """
    Handles form submission and displays the result.

    :param username: str, the Lichess username
    :param study_url: str, the URL of the Lichess study
    :param max_games: int, the number of games to look at the user's history
    :return: None
    """

    # Fetch the last game played by the user
    test_game_str = get_last_games_pgn(username, max_games)
    test_game_list = pgn_to_pgn_list(test_game_str)

    # Find deviation between games
    for game in test_game_list:
        deviation_info = find_deviation_in_entire_study(study_url, game, username)
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
