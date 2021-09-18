"""
Config project application file
"""

from dotenv import load_dotenv
import streamlit as st
import os


@st.cache()
def get_url() -> str:
    load_dotenv()
    return os.environ['MONGO_URL']
