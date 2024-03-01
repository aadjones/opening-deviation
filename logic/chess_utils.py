import chess.pgn
import io
import os
from typing import Optional, Tuple
from .deviation_result import DeviationResult

def find_deviation(repertoire_game: chess.pgn.Game, recent_game: chess.pgn.Game) -> Optional[DeviationResult]:
    """
    Compares the moves of a recent game against a repertoire game and finds the first move that deviates.

    :param repertoire_game: chess.pgn.Game, the opening repertoire game
    :param recent_game: chess.pgn.Game, the recent game to compare against the repertoire
    :return: DeviationResult, or None if there's no deviation
    """
    # Initialize a board for each game to track the position
    repertoire_board = repertoire_game.board()
    recent_board = recent_game.board()

    # Iterate through moves of both games simultaneously
    for move_number, (rep_move, recent_move) in enumerate(zip(repertoire_game.mainline_moves(), recent_game.mainline_moves()), start=1):
        player_color = 'White' if recent_board.turn else 'Black'
        # Whole move count for display; move_number will be measured in ply (half-moves)
        whole_move_number = (move_number + 1) // 2

        # Compare moves before pushing them to the board
        if rep_move != recent_move:
            # Since the move has not been made yet, the board is in the correct state to check for legality and generate SAN
            assert recent_move in recent_board.legal_moves, f'Illegal move: {recent_move} at position {recent_board.fen()}'
            deviation_san = recent_board.san(recent_move)
            reference_san = repertoire_board.san(rep_move)

            # Now, return the whole move number and the SAN notation of the deviating move from the recent game
            return DeviationResult(whole_move_number, deviation_san, reference_san, player_color)

        # If the moves are the same, then push them to their respective boards
        recent_board.push(recent_move)
        repertoire_board.push(rep_move)

    # If we reach the end without finding a deviation, return None
    return None


def pgn_string_to_game(pgn_str: str) -> chess.pgn.Game:
    """
    Converts a PGN format string into a chess.pgn.Game object.

    :param pgn_str: str, the PGN format string of the game
    :return: chess.pgn.Game, the game object
    """
    pgn_io = io.StringIO(pgn_str)
    game = chess.pgn.read_game(pgn_io)
    return game


def write_pgn(pgn_data: str, filename: str) -> None:
    """
    Writes the PGN data to a file.

    :param pgn_data: str, the PGN data to be written to the file
    :param filename: str, the name of the file to write the PGN data to
    :return: None
    """
    full_path = os.path.join(os.getcwd(), filename) 

    # Open the file in write mode (wb for binary) and write the PGN data
    with open(full_path, 'wb') as f:
        f.write(pgn_data.encode())  # Convert string to bytes

    #Print confirmation message
    print(f'PGN data successfully saved to: {full_path}')

def read_pgn(pgn_file_path: str) -> chess.pgn.Game:
    """
    Reads a PGN file and returns the corresponding chess game object.

    :param pgn_file_path: str, the path to the PGN file
    :return: chess.pgn.Game, the chess game object read from the PGN file
    """
    with open(pgn_file_path, 'r', encoding='utf-8') as pgn_file:
        return chess.pgn.read_game(pgn_file)