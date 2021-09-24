import streamlit as st
import extra_streamlit_components as stx
from App.Pages.home import home_render
from App.Pages.Components.load import load_style, load_template


def render() -> None:
    """
    Initial *render*

    :return: None
    """

    # Load streamlit page configs like title, icon, and others...
    st.set_page_config(
        page_title='Streetor',
        page_icon='🚗',
        layout='centered',
        initial_sidebar_state='collapsed'
    )

    # Load style templates .css
    load_style('App/Template/global.css')
    load_style('App/Template/st-radio.css')
    load_style('App/Template/st-button.css')

    # Init Cookie Manager that let use cookies section
    cookies = stx.CookieManager()

    if not hasattr(st, 'accepted_cookies'):
        _, s2, _ = st.columns([1, 5, 1])
        container = s2.empty()
        with container.form('cookie_form'):
            st.header('Cookies')
            st.write('By using this website, you automatically accept that we use cookies.')
            st.caption('disagree is not an option')
            res = st.form_submit_button('Understood')
        if res:
            st.accepted_cookies = True
            cookies.set('route', 'home')
            container.empty()

    # if not hasattr(st, 'route'):
    #     st.route = 'home'
    # route = getattr(st, 'route')

    route = cookies.get('route')

    # Check the 'route'
    if (route == 'home') | (route is None):
        # Render home page
        home_render(cookies)
    else:
        # Render API page
        st.warning('DB')
        x = st.button('click')
        st.write(x)
        if st.button('Back'):
            cookies.set('route', 'home')
