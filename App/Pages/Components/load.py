import streamlit as st
import streamlit.components.v1 as components


def load_style(file_name):
    with open(file_name) as f:
        st.markdown('<style>{}</style>'.format(f.read()), unsafe_allow_html=True)


def load_component(file_name):
    with open(file_name) as f:
        components.html(f.read(), height=100)


def load_template(file_name):
    with open(file_name) as f:
        st.markdown('{}'.format(f.read()), unsafe_allow_html=True)