"""
Module of load functions template/styles
"""

import streamlit as st
import streamlit.components.v1 as components


def load_style(file_name) -> None:
    """
    Load a CSS file in style page
    :param file_name: Path of CSS file
    :return: None
    """

    with open(file_name, encoding='utf-8') as style_file:
        st.markdown(f'<style>{style_file.read()}</style>', unsafe_allow_html=True)


def load_component(file_name, height=100) -> None:
    """
    Load a html/css/js file like component

    :param height: height of component (pixels)
    :param file_name: Path of HTML/CSS/JS file
    :return: None
    """

    with open(file_name, encoding='utf-8') as component_file:
        components.html(component_file.read(), height=height)


def load_template(file_name) -> None:
    """
    Load HTML file, unlike *load_component*, load_template just load a link style

    :param file_name: Path of HTML file
    :return: None
    """

    with open(file_name, encoding='utf-8') as template_file:
        st.markdown(template_file.read(), unsafe_allow_html=True)
