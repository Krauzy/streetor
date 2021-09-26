"""
Home page settings, render and config

> home_render - Render the home page
"""

import streamlit as st
from App.Pages.Components.map import scatterplot_map
from App.Pages.Components.load import load_component
from App.Database.db import get
from App.Data.single import load_model, run_model


def home_render(cookies) -> None:
    """
    Home application *render*

    :param cookies: cookies manager
    :return: Name route
    """

    # SIDEBAR PANEL

    st.sidebar.title('🔧 Settings')
    st.sidebar.markdown('---')

    # Map settings section
    with st.sidebar.expander('🗺️ Map'):
        st.caption('Settings of map display')
        st.markdown('---')
        _theme = st.selectbox(label='Theme',
                              options=[
                                  'Dark',
                                  'White',
                                  'Default'
                              ],
                              index=0)
        _real = st.color_picker(label='Primary color',
                                value='#7D28C9')
        _predict = st.color_picker(label='Secondary color',
                                   value='#DC2F02')

    # Model settings section
    with st.sidebar.expander('⚙️ Model'):
        st.caption('Settings of IA model')
        st.markdown('---')
        _clusters = st.select_slider(label='Number of Clusters',
                                     options=range(0, 251),
                                     value=100)

        if _clusters < 20 and _clusters != 0:
            st.warning('Very low number of clusters')
        elif _clusters > 150:
            st.warning('Very high number of clusters')
        elif _clusters == 0:
            st.warning('Number of clusters will be set by Streetor')

        _k = st.select_slider(label='K value',
                              options=range(1, 6),
                              value=1)

    with st.sidebar.expander('💾 Database'):
        st.caption('Settings and Visualization Data')
        st.markdown('---')
        st.checkbox(label='Only fatality accidents', value=False)
        st.checkbox(label='Only streets', value=False)
        st.markdown('---')
        st.slider('Period', 2007, 2021, (2010, 2021), 1)
        st.markdown('---')

        if st.button('⚡ API'):
            cookies.set('route', 'db')
            st.experimental_rerun()

    # MAIN PANEL

    st.title('Streetor 🚗')
    st.caption('The best way to deal with a problem')
    st.markdown('---')
    _show = st.selectbox(label='',
                         options=[
                             '🗺️ Map',
                             '📊 Graph'
                         ])

    with st.empty():
        load_component('App/Template/loading.html')
        model = load_model(
            {
                '_id': 0,
                'CITY': 0,
                'PLACE': 0,
                'WEEK': 0,
                'PERIOD': 0,
                'ROAD': 0,
                'VEHICLE': 0
            },
            {
                'CITY': 'PRESIDENTE PRUDENTE',
                'WEEK': 'FRIDAY',
                'PERIOD': 'EVENING'
            }
        )
        data, infos = run_model(model)
        st.plotly_chart(scatterplot_map(data, theme='carto-darkmatter', colors=['#6717AD']))
    st.write('ACC: ', infos['ACC'])
    st.write('R2: ', infos['R2'])
    st.write('MAE: ', infos['MAE'])
    return
