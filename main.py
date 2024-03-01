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
    study_url = st.text_input(label='Enter the URL of your Lichess public study')
    study_chapter = st.text_input(label='Enter the Chapter number of your Lichess study')
    submit_button = st.form_submit_button(label='Submit')

# Handling form submission
if submit_button:
    handle_form_submission(username, study_url, study_chapter)
