"""
This module provides the logic for the user input/output on the website through streamlit.
"""

from typing import Optional
import chess
import chess.svg
from chess.svg import Arrow
import base64
import streamlit as st
from .lichess_api import get_last_games_pgn
from .chess_utils import (
    pgn_to_pgn_list,
    find_deviation_in_entire_study_white_and_black,
)
from .deviation_result import DeviationResult


def handle_form_submission(
    username: str, study_url_white: str, study_url_black: str, max_games: int
) -> None:
    """
    Handles form submission and displays the result.

    :param username: str, the Lichess username
    :param study_url_white: str, the URL of the White Lichess study
    :param study_url_white: str, the URL of the Black Lichess study
    :param max_games: int, the number of games to look at the user's history
    :return: None
    """

    # Fetch the last game played by the user
    test_game_str = get_last_games_pgn(username, max_games)
    test_game_list = pgn_to_pgn_list(test_game_str)

    # Find deviation between games
    for game in test_game_list:
        deviation_info = find_deviation_in_entire_study_white_and_black(
            study_url_white, study_url_black, game, username
        )
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
        board_svg = get_board_svg_with_arrows(
            deviation_info.board, ref_move, dev_move, color
        )
        board_image = svg_to_image_with_base64(board_svg)
        st.image(
            board_image, caption="Red = game move; Blue = repertoire move"
        )

        # For example, move 2 will be 2. if White or 2... if Black
        periods = "." if color == "White" else "..."
        dev_move_notation = f"{i}{periods}{dev_move}"
        ref_move_notation = f"{i}{periods}{ref_move}"
        st.write(f"Deviating move: {dev_move_notation}")
        st.write(f"Reference move: {ref_move_notation}")
    else:
        st.write("No deviation found in this game.")


def svg_to_image_with_base64(svg: str) -> str:
    """
    Converts SVG string to format compatible with st.image using base64 encoding.
    :param svg: str, a string with svg data
    :return str, the converted output format that is compatible with st.image
    """
    # Encode SVG string to base64
    svg_base64 = base64.b64encode(svg.encode("utf-8")).decode("utf-8")
    # Create a base64 data URL
    return f"data:image/svg+xml;base64,{svg_base64}"


def san_to_arrow(
    board: chess.Board, move_san: str, color: str = "blue"
) -> Arrow:
    """
    Converts a move in Standard Algebraic Notation (SAN) to an Arrow object.
    :param board: chess.Board, a board state
    :param move_san: str, the SAN for the move to draw an Arrow along
    :param color: str, the color of the arrow. Defaults to blue.
    :return: Arrow, the object containing the arrow data
    """
    move = board.parse_san(move_san)
    move_uci = move.uci()
    start_square = chess.parse_square(move_uci[:2])
    end_square = chess.parse_square(move_uci[2:4])
    return Arrow(start_square, end_square, color=color)


def get_board_svg_with_arrows(
    board: chess.Board, rep_move: str, game_move: str, color: str
) -> str:
    """
    Draws arrows for the repertoire move (in red) and the game move (in blue).
    :param board: chess.Board, a board state
    :param rep_move: str, the repertoire move in SAN
    :param game_move: str, the played move in SAN
    :param color: str, either "White" or "Black"
    :return: str, the svg data of the board with the arrows
    """
    arrow_1 = san_to_arrow(board, rep_move, "blue")
    arrow_2 = san_to_arrow(board, game_move, "red")

    perspective = chess.WHITE if color == "White" else chess.BLACK
    svg = chess.svg.board(
        board=board,
        arrows=[arrow_1, arrow_2],
        orientation=perspective,
        size=350,
    )
    return svg
