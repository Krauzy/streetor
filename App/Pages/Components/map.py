import plotly.express as px
import streamlit as st
from pandas import DataFrame
from plotly.graph_objects import Figure
from App.Data.geoapi import get_address


@st.cache(show_spinner=False)
def make_address(data: DataFrame):
    return data.apply(lambda x: get_address(x.LATITUDE, x.LONGITUDE), axis=1)


@st.cache(show_spinner=False)
def scatterplot_map(info: DataFrame, colors=None, theme='open-street-map') -> Figure:
    """
    Plot a scatter map built by *Plotly*

    :param info: DataFrame info data
    :param colors: Array of colors
    :param theme: theme name
    :return: The map plotted
    """
    if colors is None:
        colors = ['#DC2F02', '#7D28C9']
    # info = info[info['TARGET'] == 'PREDICT']
    # print(len(info))
    # if len(info) < 100:
    #    info['ADDRESS'] = make_address(info)
    # else:
    #    info['ADDRESS'] = 'NOT AVAILABLE'
    fig = px.scatter_mapbox(info,
                            lat="LATITUDE",
                            lon="LONGITUDE",
                            color_discrete_sequence=colors,
                            # color='TARGET',
                            hover_name='TARGET',
                            hover_data=['WEEK', 'PERIOD'],
                            height=500,
                            width=704,
                            zoom=10,
                            mapbox_style=theme)
    fig.update_layout(margin={'r': 0, 't': 0, 'l': 0, 'b': 0})
    return fig
