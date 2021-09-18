import plotly.express as px
import streamlit as st
from plotly.graph_objects import Figure


@st.cache()
def plot_map(info, colors=None, theme='open-street-map') -> Figure:
    """
    Plot a scatter map built by *Plotly*

    :param info: DataFrame
    :param colors: Array
    :param theme: str
    :return: The map plotted
    """
    if colors is None:
        colors = ['#DC2F02', '#7D28C9']
    fig = px.scatter_mapbox(info,
                            lat="Latitude",
                            lon="Longitude",
                            color_discrete_sequence=colors,
                            color='Target',
                            hover_name='Target',
                            # hover_data=['Victim', 'Day of Week', 'Hour', 'Year'],
                            height=500,
                            width=810,
                            zoom=10,
                            mapbox_style=theme)
    return fig
