import streamlit as st
from App.Pages.Components.map import plot_map


def home_render() -> None:
    """
    Home application *render*

    :return: Name route
    """
    st.sidebar.title('🔧 Settings')
    st.sidebar.markdown('---')

    with st.sidebar.expander('🗺️ Map'):
        st.caption('Settings of map display')
        st.markdown('---')
        g_theme = st.selectbox(label='Theme',
                               options=['Dark', 'White', 'Default'],
                               index=0)
        g_real = st.color_picker(label='Primary color',
                                 value='#7D28C9')
        g_predict = st.color_picker(label='Secondary color',
                                    value='#DC2F02')

    with st.sidebar.expander('⚙️ Model'):
        st.caption('Settings of IA model')
        # st.text(' ')
        st.markdown('---')
        g_clusters = st.select_slider(label='Number of Clusters',
                                      options=range(0, 251),
                                      value=100)

        if g_clusters < 20 and g_clusters != 0:
            st.warning('Very low number of clusters')
        elif g_clusters > 150:
            st.warning('Very high number of clusters')
        elif g_clusters == 0:
            st.warning('Number of clusters will be set by Streetor')

        g_k = st.select_slider(label='K value',
                               options=range(1, 6),
                               value=1)

    st.title('Streetor 🚗')
    st.caption('The best way to deal with a problem')
    st.markdown('---')
    show = st.selectbox(label='',
                        options=['🗺️ Map', '📊 Graph'])
    # st.plotly_chart(plot_map(None))
    return
