from src.static.single import Single
from src.pages.home import render_home
from src.pages.database import render_database
import streamlit as st

st.set_page_config(
    page_title='Streetor',
    page_icon='🚗',
    layout='centered',
    initial_sidebar_state='collapsed'
)

def route():
    if Single.get_instance().route == 'Home':
        render_home()
    else:
        render_database()