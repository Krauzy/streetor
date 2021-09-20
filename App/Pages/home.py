import streamlit as st
from App.Pages.Components.map import plot_map
from App.Pages.Components.load import load_component
from App.Database.db import get


def home_render(cookies) -> None:
    """
    Home application *render*

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

    if st.sidebar.button('DB'):
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
        st.dataframe(get(fields={'_id': 0}, limit=2000))
    # st.plotly_chart(plot_map(None))
    return
