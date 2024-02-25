import streamlit as st
import requests
import chess.pgn
import chess
import os
import io
import time

api_token = st.secrets["LICHESS_API_TOKEN"]

def get_last_games_pgn(username, max_games=1, retries=3, backoff_factor=1.5, timeout=10):
    """Fetch the PGN of the last game played by a Lichess username with retry and timeout.

    :return PGN string
    """
    url = f'https://lichess.org/api/games/user/{username}'
    params = {'max': max_games}  # Fetch only the most recent game
    headers = {'Accept': 'application/x-chess-pgn'}

    for attempt in range(retries):
        try:
            response = requests.get(url, params=params, headers=headers, timeout=timeout)
            
            if response.status_code == 200:
                return response.text
            elif response.status_code == 429:
                wait = backoff_factor * (2 ** attempt)
                print(f"Rate limit exceeded. Waiting {wait} seconds before retrying...")
                time.sleep(wait)
            else:
                return f"Failed to fetch games. Status code: {response.status_code}"
        except requests.exceptions.Timeout:
            print(f"Request timed out. Attempt {attempt + 1} of {retries}.")
        except requests.exceptions.RequestException as e:
            return f"An error occurred: {str(e)}"

    return "Failed to retrieve the PGN after several attempts."


def find_deviation(repertoire_game, recent_game):
    """
    Compares the moves of a recent game against a repertoire game and finds the first move that deviates.
    Now using whole move numbers in chess notation.

    :param repertoire_game: chess.pgn.Game, the opening repertoire game
    :param recent_game: chess.pgn.Game, the recent game to compare against the repertoire
    :return: tuple, (whole move number, move in SAN format) of the first deviation, or None if there's no deviation
    """
    # Initialize a board for each game to track the position
    repertoire_board = repertoire_game.board()
    recent_board = recent_game.board()

    # Iterate through moves of both games simultaneously
    for move_number, (rep_move, recent_move) in enumerate(zip(repertoire_game.mainline_moves(), recent_game.mainline_moves()), start=1):
        player_color = "White" if recent_board.turn else "Black"
        # Whole move count for display
        whole_move_number = (move_number + 1) // 2

        # Compare moves before pushing them to the board
        if rep_move != recent_move:
            # Since the move has not been made yet, the board is in the correct state to check for legality and generate SAN
            assert recent_move in recent_board.legal_moves, f"Illegal move: {recent_move} at position {recent_board.fen()}"
            deviation_san = recent_board.san(recent_move)
            reference_san = repertoire_board.san(rep_move)

            # Now, return the whole move number and the SAN notation of the deviating move from the recent game
            return whole_move_number, deviation_san, reference_san, player_color

        # If the moves are the same, then push them to their respective boards
        recent_board.push(recent_move)
        repertoire_board.push(rep_move)

    # If we reach the end without finding a deviation, return None
    return None



def pgn_string_to_game(pgn_str):
    """
    Converts a PGN format string into a chess.pgn.Game object.

    :param pgn_str: str, the PGN format string of the game
    :return: chess.pgn.Game, the game object
    """
    pgn_io = io.StringIO(pgn_str)
    game = chess.pgn.read_game(pgn_io)
    return game

def write_pgn(pgn_data, filename):
    full_path = os.path.join(os.getcwd(), filename) 

    # Open the file in write mode (wb for binary) and write the PGN data
    with open(full_path, "wb") as f:
        f.write(pgn_data.encode())  # Convert string to bytes

    #Print confirmation message
    print(f"PGN data successfully saved to: {full_path}")

def read_png(pgn_file_path):
    with open(pgn_file_path, 'r', encoding='utf-8') as pgn_file:
        return chess.pgn.read_game(pgn_file)


################################################################################

username = "jrjrjr4"
# max_games = 1
# test_game_str = get_last_games_pgn(username, max_games) # pgn string type
# write_pgn(test_game_str, "jrjrjr4-last-game.pgn") # useful for debugging
# test_game = pgn_string_to_game(test_game_str) # convert to Game type

pgn_path = "pgns/"

test_game_path = pgn_path + "jrjrjr4-last-game.pgn"
test_game = read_png(test_game_path)

ref_file_path = pgn_path + "filipowicz-borkowski.pgn"

reference_game = read_png(ref_file_path)

i, move, ref_move, color = find_deviation(reference_game, test_game)
periods = "." if color == "White" else "..."
move_notation = f"{i}{periods}{move}"
ref_move_notation = f"{i}{periods}{ref_move}"
print(f"First game move that deviated from reference: {move_notation}")
print(f"Reference move: {ref_move_notation}")


################################################################################

# Title of the web app
st.title('Chess Opening Repertoire Practice')

# Input form
with st.form(key='my_form'):
    username = st.text_input(label='Enter your Lichess username')
    study_url = st.text_input(label='Enter the URL of your Lichess public study')
    submit_button = st.form_submit_button(label='Submit')

# Handling form submission
if submit_button:
    # Here you can add the code to handle the username and study URL
    # For example, you can call functions that fetch the user's games and the study data
    # and then process and display the results.
    st.write(f'Hello {username}, you submitted the study URL: {study_url}')
    # ... (Your processing and result display logic here)

