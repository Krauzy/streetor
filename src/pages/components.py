import streamlit as st

def load_component(body):
    """
    Carrega um componente HTML/CSS na página
    :param body: Conteúdo HTML/CSS a ser carregado como component
    """
    st.markdown(body, unsafe_allow_html=True)

def set_radio_horizontal():
    """
    Carrega a estilização que deixa o componente [radioButton] na horizontal
    :return: None
    """
    st.markdown('<style>div.row-widget.stRadio > div{flex-direction:row; gap: 15px;}</style>', unsafe_allow_html=True)
