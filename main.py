"""
This is the driver code that actually displays the website through streamlit.
"""
import streamlit as st
from logic.form_handlers import handle_form_submission

################################################################################
# Global variables
################################################################################

# PGN_PATH = 'pgns/' # useful for debugging to read/write pgn files

# api_token = st.secrets["LICHESS_API_TOKEN"] # api token may be necessary later

################################################################################
# End of global variables
################################################################################


# Title of the web app
st.title('Chess Opening Repertoire Practice')

# Input form
with st.form(key='opening_form'):
    username = st.text_input(label='Enter your Lichess username')
    study_url_white = st.text_input(label='Enter the URL of your White Lichess study')
    study_url_black = st.text_input(label='Enter the URL of your Black Lichess study')
    max_games = st.text_input(label='Enter number of games to analyze')
    submit_button = st.form_submit_button(label='Submit')

# Handling form submission
if submit_button:
    handle_form_submission(username, study_url_white, study_url_black, int(max_games))
