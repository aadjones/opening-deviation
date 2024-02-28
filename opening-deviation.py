import streamlit as st
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import chess.pgn
import chess
import os
import io
from typing import Optional, Tuple, IO

################################################################################
# Global variables
################################################################################

PGN_PATH = "pgns/" # useful for debugging to read/write pgn files

# api_token = st.secrets["LICHESS_API_TOKEN"] # api token may be necessary later

################################################################################
# End of global variables
################################################################################

################################################################################
# Function definitions
################################################################################

def get_last_games_pgn(username: str, max_games: int = 1, retries: int = 3,
                       backoff_factor: float = 1.5, timeout: int = 10) -> Optional[str]:
    """
    Fetches the PGN of the last several games played by a Lichess username with retry and timeout.

    :param username: str, the Lichess username of the player
    :param max_games: int, the maximum number of games to retrieve (default is 1)
    :param retries: int, the number of retries in case of failures (default is 3)
    :param backoff_factor: float, the backoff factor for retrying requests (default is 1.5)
    :param timeout: int, the timeout for each HTTP request in seconds (default is 10)
    :return: Optional[str], the PGN content of the last game(s) played by the user, or None if failed
    """
    session = requests.Session()
    retry = Retry(total=retries, read=retries, connect=retries, backoff_factor=backoff_factor,
                  status_forcelist=(500, 502, 504))
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('https://', adapter)

    try:
        response = session.get(f'https://lichess.org/api/games/user/{username}',
                               params={'max': max_games}, timeout=timeout)
        response.raise_for_status()  # Will raise an HTTPError if the HTTP request returned an unsuccessful status code
        return response.text
    except requests.exceptions.RequestException as e:
        print(f'An error occurred: {e}')
        return None


def find_deviation(repertoire_game: chess.pgn.Game, recent_game: chess.pgn.Game) -> Optional[Tuple[int, str, str, str]]:
    """
    Compares the moves of a recent game against a repertoire game and finds the first move that deviates.

    :param repertoire_game: chess.pgn.Game, the opening repertoire game
    :param recent_game: chess.pgn.Game, the recent game to compare against the repertoire
    :return: tuple, (whole move number, deviation move in SAN format, reference move in SAN format, player color str), or None if there's no deviation
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
            return whole_move_number, deviation_san, reference_san, player_color

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
    
def get_pgn_from_study(study_url: str, chapter_number: int) -> str:
    """
    Extracts the PGN from a specified chapter of a Lichess study using the Lichess API.

    :param study_url: str, the url of the Lichess study
    :param chapter_number: int, the chapter number from which to extract the PGN
    :return: str, the PGN data
    """
    # Construct the URL for fetching study details
    study_id = extract_study_id_from_url(study_url)
    url = f'https://lichess.org/api/study/{study_id}.pgn'

    # Unclear if we need all these parameters inside params below; could just be a ChatGPT thing
    params = {
        'clocks': 'false',
        'comments': 'true',
        'variations': 'true',
        'source': 'false',
        'orientation': 'false'
    }

    # Fetch study details from the Lichess API
    response = requests.get(url, params=params)
    if response.status_code != 200:
        return f'Failed to fetch study. Status code: {response.status_code}'

    # Extract the PGN data for the entire study
    full_pgn_data = response.text
    
    # Extract the PGN data for the specified chapter
    chapter_pgn = extract_chapter_pgn(full_pgn_data, chapter_number)  
    return chapter_pgn

def extract_study_id_from_url(url: str) -> str:
    """
    Extracts the study ID from a Lichess study URL.

    :param url: str, the URL of the Lichess study
    :return: str, the study ID extracted from the URL
    """
    parts = url.split('/')
    # The study ID is the third part of the URL
    # For example, after the split, the parts variable will contain
    # ['https:', '', 'lichess.org', 'study', 'RKEBYTWL', 'muR4Kgyc']
    # and we want to grab 'RKEBYTWL', which is at index 4
    study_id = parts[4]  
    return study_id

def extract_chapter_pgn(full_pgn: str, chapter_number: int) -> str:
    """
    Extracts the PGN for a specific chapter from the full PGN data.

    :param full_pgn: str, the entire PGN data from the study
    :param chapter_number: int, the chapter number to extract
    :return: str, the PGN for the specified chapter or an error message if not found
    """
    chapters = full_pgn.strip().split('\n\n\n')
    if chapter_number > len(chapters) or chapter_number < 1:
        return f'Chapter {chapter_number} not found in the study.'

    # Chapters are 1-indexed, but lists are 0-indexed
    chapter_pgn = chapters[chapter_number - 1].strip()
    
    # Check if the chapter PGN starts with a PGN tag; if not, it might not be a valid PGN
    # This part of the code might be too brittle; do all PGN files start with '[Event'?
    if not chapter_pgn.startswith('[Event'):
        return f'Chapter {chapter_number} PGN not found or not valid.'
    
    return chapter_pgn

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
   

def display_deviation_info(deviation_info: Optional[Tuple[int, str, str, str]]) -> None:
    """
    Displays the deviation information.

    :param deviation_info: tuple or None, information about the deviation
    :return: None
    """
    if deviation_info:
        i, move, ref_move, color = deviation_info
        periods = '.' if color == 'White' else '...' # For example, move 2 will be 2. if White or 2... if Black
        move_notation = f'{i}{periods}{move}'
        ref_move_notation = f'{i}{periods}{ref_move}'
        st.write(f'First game move from your last game played that deviated from reference study: {move_notation}')
        st.write(f'Reference move: {ref_move_notation}')
    else:
        st.write('No deviation found in the last game played.')

################################################################################
# End of function definitions
################################################################################

################################################################################
# Driver code
################################################################################

if __name__ == '__main__':
    # Title of the web app
    st.title('Chess Opening Repertoire Practice')

    # Input form
    with st.form(key='opening_form'):
        username = st.text_input(label='Enter your Lichess username')
        study_url = st.text_input(label='Enter the URL of your Lichess public study')
        study_chapter = st.text_input(label='Enter the Chapter number of your Lichess study')
        submit_button = st.form_submit_button(label='Submit')

    # Handling form submission
    if submit_button:
        handle_form_submission(username, study_url, study_chapter)
        
