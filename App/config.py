"""
Config project application file
"""

from dotenv import load_dotenv
import streamlit as st
import os


def get_url() -> str:
    """
    Get the URL connection of MongoDB database access by *environment variable*

    :return: URL connection
    """
    # Check if dotenv just was loaded
    if not hasattr(st, 'dotenv_loaded'):
        # Load python-dotenv configs
        load_dotenv()
        st.dotenv_loaded = True
    return os.environ['MONGO_URL']


def get_token() -> str:
    """
    Get the *TOKEN* of API *positionstack*

    :return: Token
    """

    # Check if dotenv just was loaded
    if not hasattr(st, 'dotenv_loaded'):
        # Load python-dotenv configs
        load_dotenv()
        st.dotenv_loaded = True
    return os.environ['TOKEN_KEY_API']
