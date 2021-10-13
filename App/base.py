"""
base render page
"""

import streamlit as st
import extra_streamlit_components as stx
from App.Pages.home import home_render
from App.Pages.Components.load import load_style, load_template


def render():
    """
    Initial *render*

    :return: None
    """

    # Load streamlit page configs like title, icon, and others...
    about_info = ''' ## 🚗 Streetor App
    ---
    This app uses ML model with `KMeans` and `KNN` to predict accidents locations in urban zones 
    
    ⚡[View on Github](https://github.com/Krauzy)⚡'''
    st.set_page_config(
        page_title='Streetor',
        page_icon='🚗',
        layout='centered',
        initial_sidebar_state='collapsed',
        menu_items={'About': about_info}
    )

    # Load style templates .css
    load_style('App/Template/global.css')
    load_style('App/Template/st-radio.css')
    load_style('App/Template/st-button.css')
    load_template('App/Template/poppins.html')

    # Init Cookie Manager that let use cookies section
    cookies = stx.CookieManager()

    # route = cookies.get('route')

    # if (route is None) | (not hasattr(st, 'accepted_cookies')):
    #     _, col, _ = st.columns([1, 5, 1])
    #     container = col.empty()
    #     with container.form('cookie_form'):
    #         st.header('Cookies')
    #         st.write('By using this website, you automatically accept that we use cookies.')
    #         st.caption('disagree is not an option')
    #         res = st.form_submit_button('Understood')
    #     if res:
    #         st.accepted_cookies = True
    #         cookies.set('route', 'home')
    #         container.empty()

    # if not hasattr(st, 'route'):
    #     st.route = 'home'
    # route = getattr(st, 'route')

    route = cookies.get('route')

    # Check the 'route'
    if (route is None) | (route == 'home'):
        # Render home page
        home_render(cookies)
    # elif route == 'api':
    #     # Render API page
    #     st.warning('DB')
    #     res = st.button('click')
    #     st.write(res)
    #     if st.button('Back'):
    #         cookies.set('route', 'home')
