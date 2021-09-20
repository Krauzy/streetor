import streamlit as st
from App.Pages.home import home_render
from App.Pages.Components.load import load_style
import extra_streamlit_components as stx


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

    load_style('App/Template/global.css')
    load_style('App/Template/st-radio.css')
    load_style('App/Template/st-button.css')

    cookies = stx.CookieManager()
    route = cookies.get('route')
    if (route is None) | (route == 'home'):
        home_render(cookies)
    else:
        st.warning('DB')
        if st.button('Back'):
            cookies.set('route', 'home')
