"""
This module handles requests to the Lichess API to get the last games from a username
and get study data from a Lichess study.
"""

from typing import Optional
import re
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


def get_last_games_pgn(
    username: str,
    max_games: int = 1,
    retries: int = 3,
    backoff_factor: float = 1.5,
    timeout: int = 10,
) -> Optional[str]:
    """
    Fetches the PGN of the last several games played by a Lichess username with retry and timeout.

    :param username: str, the Lichess username of the player
    :param max_games: int, the maximum number of games to retrieve (default is 1)
    :param retries: int, the number of retries in case of failures (default is 3)
    :param backoff_factor: float, the backoff factor for retrying requests (default is 1.5)
    :param timeout: int, the timeout for each HTTP request in seconds (default is 10)
    :return: Optional[str], the PGN of the last game(s) played by the user, or None if failed
    """
    session = requests.Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=(500, 502, 504),
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("https://", adapter)

    try:
        response = session.get(
            f"https://lichess.org/api/games/user/{username}",
            params={"max": max_games},
            timeout=timeout,
        )
        # Will raise an HTTPError if the HTTP request returned an unsuccessful status code
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None


def get_pgn_from_study(study_url: str, chapter_number: int) -> str:
    """
    Extracts the PGN from a specified chapter of a Lichess study using the Lichess API.

    :param study_url: str, the url of the Lichess study
    :param chapter_number: int, the chapter number from which to extract the PGN
    :return: str, the PGN data
    """
    # Construct the URL for fetching study details
    study_id = extract_study_id_from_url(study_url)
    url = f"https://lichess.org/api/study/{study_id}.pgn"

    # Unclear if we need all these parameters inside params below; could just be a ChatGPT thing
    params = {
        "clocks": "false",
        "comments": "true",
        "variations": "true",
        "source": "false",
        "orientation": "false",
    }

    # Fetch study details from the Lichess API
    response = requests.get(url, params=params, timeout=10)
    if response.status_code != 200:
        return f"Failed to fetch study. Status code: {response.status_code}"

    # Extract the PGN data for the entire study
    full_pgn_data = response.text

    # Extract the PGN data for the specified chapter
    chapter_pgn = extract_chapter_pgn(full_pgn_data, chapter_number)
    return chapter_pgn


def extract_study_id_from_url(url: str) -> str:
    """
    Extracts the study ID from a Lichess study URL.

    :param url: str, the URL of the Lichess study
    :return: str, the study ID extracted from the URL, or an empty string if not found
    """
    # Use a regex pattern to match the study ID in the URL
    pattern = re.compile(r"lichess\.org/study/([a-zA-Z0-9]+)")
    match = pattern.search(url)

    if match:
        # The study ID is captured in the first group of the match
        return match.group(1)

    # Return an empty string or a specific message if the URL doesn't match the expected format
    return "Study ID not found"


def extract_chapter_pgn(full_pgn: str, chapter_number: int) -> str:
    """
    Extracts the PGN for a specific chapter from the full PGN data.

    :param full_pgn: str, the entire PGN data from the study
    :param chapter_number: int, the chapter number to extract
    :return: str, the PGN for the specified chapter or an error message if not found
    """
    chapters = full_pgn.strip().split("\n\n\n")
    if chapter_number > len(chapters) or chapter_number < 1:
        return f"Chapter {chapter_number} not found in the study."

    # Chapters are 1-indexed, but lists are 0-indexed
    chapter_pgn = chapters[chapter_number - 1].strip()

    # Check if the chapter PGN starts with a PGN tag; if not, it might not be a valid PGN
    # This part of the code might be too brittle; do all PGN files start with '[Event'?
    if not chapter_pgn.startswith("[Event"):
        return f"Chapter {chapter_number} PGN not found or not valid."

    return chapter_pgn


def get_study_chapters_count(study_id: str) -> int:
    """
    Gets the number of chapters in a Lichess study.

    :param study_id: str, the url for a Lichess study
    :return: int, the number of chapters in the study
    """
    url: str = f"https://lichess.org/api/study/{study_id}.pgn"
    response: requests.Response = requests.get(url)
    if response.status_code != 200:
        return f"Failed to fetch study. Status code: {response.status_code}"

    # Extract the PGN data for the entire study
    full_pgn_data = response.text
    chapters = full_pgn_data.strip().split("\n\n\n")
    return len(chapters)
