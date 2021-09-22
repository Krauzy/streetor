"""
Config project application file
"""

from dotenv import load_dotenv
import streamlit as st
import os


@st.cache()
def get_url() -> str:
    """
    Get the URL connection of MongoDB database access by *environment variable*

    :return: URL connection
    """
    # Load python-dotenv configs
    load_dotenv()
    return os.environ['MONGO_URL']
