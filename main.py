"""
This is the driver code that actually displays the website through streamlit.
"""

import streamlit as st
from logic.form_handlers import handle_form_submission_grid

################################################################################
# Global variables
################################################################################

# PGN_PATH = 'pgns/' # useful for debugging to read/write pgn files

# api_token = st.secrets["LICHESS_API_TOKEN"] # api token may be necessary later

################################################################################
# End of global variables
################################################################################

# Title of the web app
st.title("Chess Opening Repertoire Practice")

# Input form
with st.form(key="opening_form"):
    # Defaults
    DEFAULT_USERNAME = "Jrjrjr4"
    DEFAULT_WHITE_STUDY = "https://lichess.org/study/14RZiFdX/fvGLXd1D"
    DEFAULT_BLACK_STUDY = "https://lichess.org/study/bve0Qw48/7ZVSY8Po"

    # First row for username and max games
    col1, col2 = st.columns([3, 2])
    with col1:
        username = st.text_input(
            label="Enter your Lichess username", value=DEFAULT_USERNAME
        )
    with col2:
        max_games = st.text_input(label="Enter number of games to analyze")

    # Second row for study URLs
    col3, col4 = st.columns(2)
    with col3:
        study_url_white = st.text_input(
            label="Enter the URL of your White Lichess study",
            value=DEFAULT_WHITE_STUDY,
        )
    with col4:
        study_url_black = st.text_input(
            label="Enter the URL of your Black Lichess study",
            value=DEFAULT_BLACK_STUDY,
        )

    # Submit button in its own row to span across the form
    submit_button = st.form_submit_button(label="Submit (this will be SLOW)")

# Handling form submission
if submit_button:
    # handle_form_submission(
    #     username, study_url_white, study_url_black, int(max_games)
    # )
    handle_form_submission_grid(
        username, study_url_white, study_url_black, int(max_games)
    )
