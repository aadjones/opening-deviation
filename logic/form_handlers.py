"""
This module provides the logic for the user input/output on the website through streamlit.
"""

from typing import Optional, List
import chess
import chess.svg
from chess.svg import Arrow
import streamlit as st
from streamlit import logger
from . import lichess_api
from . import pgn_utils
from .lichess_api import get_last_games_pgn
from .chess_utils import (
    find_deviation_in_entire_study_white_and_black,
)
from .deviation_result import DeviationResult

LOG = logger.get_logger(__name__)


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
        st.markdown(board_svg, unsafe_allow_html=True)
        # For example, move 2 will be 2. if White or 2... if Black
        periods = "." if color == "White" else "..."
        dev_move_notation = f"{i}{periods}{dev_move}"
        ref_move_notation = f"{i}{periods}{ref_move}"
        st.write(f"Deviating move: {dev_move_notation}")
        st.write(f"Reference move: {ref_move_notation}")
    else:
        st.write("No deviation found in this game.")


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
        size=200,
    )
    return svg


def display_image_grid(images: List[str], max_cols: int = 4) -> None:
    """
    Displays a grid of SVG images in Streamlit, ensuring up to a
    specified maximum number of columns.

    :param images: List of SVG formatted images as strings.
    :param max_cols: Maximum number of columns in the grid. Defaults to 4.
    :return: None
    """
    cols = st.columns(max_cols)  # Prepare columns

    for idx, image in enumerate(images):
        # Assuming SVGs might need width adjustment; insert style attribute for width control
        updated_image = image.replace(
            "<svg ", '<svg style="width:100%; height:auto;" ', 1
        )

        with cols[idx % max_cols]:
            st.markdown(updated_image, unsafe_allow_html=True)


def get_image_from_deviation_info(
    deviation_info: Optional[DeviationResult],
) -> str:
    """
    Get the corresponding svg from a deviation result, or return None if there is a None input.

    :param deviation_info: DeviationResult, a deviation from your game, or None if there was no deviation
    :return: str, the svg data correpsonding to that result, or a clear board svg if there is no deviation
    """
    if deviation_info:
        dev_move = deviation_info.deviation_san
        ref_move = deviation_info.reference_san
        color = deviation_info.player_color
        board_svg = get_board_svg_with_arrows(
            deviation_info.board, ref_move, dev_move, color
        )
        return board_svg
    # Else there was no deviation
    board = chess.Board()
    board.clear()
    svg = chess.svg.board(board, size=200)
    return svg


def get_image_grid_from_deviation_list(
    deviation_list: List[Optional[DeviationResult]],
) -> List[str]:
    """
    From a list of deviations, form a list of svg outputs.

    :param deviation_list: List[Optional[DeviationResult]], the list of deviations
    :return: List[str], the svg data in a list
    """
    svg_data = [get_image_from_deviation_info(info) for info in deviation_list]
    return svg_data


def handle_form_submission_grid(
    username: str,
    study_url_white: str,
    study_url_black: str,
    max_games: int,
) -> None:
    """
    Handles form submission and displays the result in a grid

    :param username: str, the Lichess username
    :param study_url_white: str, the URL of the White Lichess study
    :param study_url_black: str, the URL of the Black Lichess study
    :param max_games: int, the number of games to look at the user's history
    :return: None
    """

    # Fetch the last game played by the user
    test_game_str = get_last_games_pgn(username, max_games)
    test_game_list = pgn_utils.pgn_to_pgn_list(test_game_str)

    white_study = lichess_api.Study.fetch_url(study_url_white)
    black_study = lichess_api.Study.fetch_url(study_url_black)

    # Find deviation between games
    info_list = []
    for game in test_game_list:
        deviation_info = find_deviation_in_entire_study_white_and_black(
            white_study, black_study, game, username
        )
        info_list.append(deviation_info)
    grid = get_image_grid_from_deviation_list(info_list)
    display_image_grid(grid)
