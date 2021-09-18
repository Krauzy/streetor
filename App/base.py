import streamlit as st
from App.Pages.home import home_render
from App.Pages.Components.load import load_template


def render() -> None:
    """
    Initial *render*

    :return: None
    """
    st.set_page_config(
        page_title='Streetor',
        page_icon='🚗',
        layout='centered',
        initial_sidebar_state='collapsed'
    )
    load_template('App/Template/global.css')
    load_template('App/Template/st-radio.css')
    load_template('App/Template/st-button.css')
    home_render()
