"""
Home page settings, render and config

> home_render - Render the home page
"""

import streamlit as st
from App.Pages.Components.map import scatterplot_map
from App.Pages.Components.load import load_component, load_style
from App.Data.single import load_model, run_model


def home_render(cookies) -> None:
    """
    Home application *render*

    :param cookies: cookies manager
    :return: Name route
    """

    load_style('App/Template/table.css')

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

        if _theme == 'Dark':
            _theme = 'carto-darkmatter'
        elif _theme == 'White':
            _theme = 'carto-positron'
        else:
            _theme = 'open-street-map'

        _primary = st.color_picker(label='Primary color',
                                   value='#7D28C9')
        _secondary = st.color_picker(label='Secondary color',
                                     value='#DC2F02')

    # Model settings section
    with st.sidebar.expander('⚙️ Model'):
        st.caption('Settings of IA model')
        st.markdown('---')
        _clusters = st.checkbox('Clusters will be set by Streetor', value=True)
        if not _clusters:
            _clusters = st.select_slider(label='Number of Clusters',
                                         options=range(1, 252),
                                         value=100)

        _k = st.select_slider(label='K value',
                              options=range(1, 6),
                              value=1)

    with st.sidebar.expander('💾 Database'):
        st.caption('Settings and Visualization Data')
        st.markdown('---')
        st.checkbox(label='Only fatality accidents',
                    value=False)
        st.checkbox(label='Only streets',
                    value=False)
        st.checkbox(label='Show address',
                    value=False,
                    help='This requires a very high cost, so it may take a while')
        st.markdown('---')
        st.slider(label='Period',
                  min_value=2007,
                  max_value=2021,
                  value=(2010, 2021),
                  step=1)
        st.markdown('---')

        if st.button('⚡ API'):
            cookies.set('route', 'api')
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
        st.plotly_chart(scatterplot_map(data, theme=_theme, colors=[_secondary]))

    st.markdown('### Information')
    with st.expander('🎯 Result'):
        st.markdown('''
            ---
            | Tag | Values |
            | ----- | ----- |
            | Accuracy | `{}` |
            | R² | `{}` |
            | Mean Absolute Error | `{}` |
            | Mean Squared Error | `{}` |
            | Root Mean Squared Error | `{}` |
            | Mean Latitude | `{}` |
            | Mean Longitude | `{}` |
            | Sum Latitude | `{}` |
            | Sum Longitude | `{}` |
        '''.format(
            str(infos['ACC']) + '%',
            str(infos['R2']) + '%',
            str(infos['MAE']),
            str(infos['MSE']),
            str(infos['RMSE']),
            str(infos['MED_LAT']),
            str(infos['MED_LON']),
            str(infos['SUM_LAT']),
            str(infos['SUM_LON'])
        ))
        st.write(' ')

    with st.expander('🤖 Machine Learning'):
        st.markdown('''
            ---
            | Tag | Values |
            | ----- | ----- |
            | K value of KNN | `{}` |
            | Number of Clusters | `{}` |
            | Distance Variance | `{} KM`|
        '''.format(
            str(infos['KNN']),
            str(infos['CLUSTERS']),
            str(infos['KM'])
        ))
        st.write(' ')

    with st.expander('💾 Data'):
        st.markdown('''
            ---
            | Tag | Values |
            | ----- | ----- |
            | City | `{}` |
            | Period | `{}` |
            | Day of Week | `{}` |
            | Total of Accidents | `{}` |
        '''.format(
            'PRESIDENTE PRUDENTE',
            str(infos['PERIOD']),
            str(infos['WEEK']),
            str(infos['TOTAL'])
        ))
        st.write(' ')

    return
