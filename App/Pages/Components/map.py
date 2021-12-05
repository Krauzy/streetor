"""
Module of plot maps on streamlit theme style
"""

import plotly.express as px
import seaborn as sns
import streamlit as st
from pandas import DataFrame, Series
from plotly.graph_objects import Figure
from App.Data.geoapi import get_address


@st.cache(show_spinner=False)
def make_address(data: DataFrame) -> Series:
    """
    Get a Series of address rest by addressAPI
    :param data: DataFrame of LATITUDE and LONGITUDE columns
    :return:
    """
    return data.apply(lambda x: get_address(x.LATITUDE, x.LONGITUDE), axis=1)


@st.cache(show_spinner=False)
def scatterplot_map(info: DataFrame,
                    colors=None,
                    theme='carto-darkmatter',
                    show_real=False,
                    address=False) -> Figure:
    """
    Plot a scatter map built by *Plotly*

    :param info: DataFrame info data
    :param colors: Array of colors (default is ['#DC2F02', '#7D28C9'])
    :param theme: theme name (default is 'carto-darkmatter')
    :param show_real: Show the real values or just the predict values (default is False)
    :param address: show url address each row data (default is False)
    :return: The map plotted
    """

    if colors is None:
        colors = ['#DC2F02', '#7D28C9']

    if not show_real:
        info = info[info['TARGET'] == 'PREDICT']

    if address:
        info['ADDRESS'] = make_address(info)
    else:
        info['ADDRESS'] = 'NOT AVAILABLE'

    fig = px.scatter_mapbox(info,
                            lat="LATITUDE",
                            lon="LONGITUDE",
                            color_discrete_sequence=colors,
                            color='TARGET',
                            hover_name='TARGET',
                            hover_data=['WEEK', 'PERIOD', 'ADDRESS'],
                            height=500,
                            width=814,
                            zoom=12,
                            mapbox_style=theme)
    fig.update_layout(margin={
        'r': 0,
        't': 0,
        'l': 0,
        'b': 0
    })
    return fig


@st.cache(show_spinner=False)
def heat_map(info: list, theme='carto-darkmatter') -> Figure:
    """
    Plot a incidence index HeatMap of traffic accidents

    :param info: list of latitude, longitude and incidence index
    :param theme: theme of background map (default is 'carto-darkmatter')
    :return: A figure of HeatMap plotted
    """

    data = DataFrame(info, columns=['LATITUDE', 'LONGITUDE', 'INCIDENCE'])
    fig = px.density_mapbox(data,
                            lat='LATITUDE',
                            lon='LONGITUDE',
                            z='INCIDENCE',
                            radius=15,
                            center=dict(
                                lat=data.iloc[0]['LATITUDE'],
                                lon=data.iloc[0]['LONGITUDE']
                            ),
                            zoom=12,
                            width=804,
                            mapbox_style=theme)
    fig.update_layout(margin={
        'r': 0,
        't': 0,
        'l': 0,
        'b': 0
    })
    return fig


@st.cache(show_spinner=False)
def bubble_map(info: list, theme='carto-darkmatter', color='#DC2F02'):
    """
    Plot a index incidence BubbleMap of size zone incidence traffic accident

    :param info: list of latitude, longitude and incidence data
    :param theme: theme of background map (default is 'carto-darkmatter')
    :param color: color of bubbles (default is '#DC2F02')
    :return: BubbleMap plotted
    """

    data = DataFrame(info, columns=['LATITUDE', 'LONGITUDE', 'INCIDENCE'])
    fig = px.scatter_mapbox(data,
                            lat="LATITUDE",
                            lon="LONGITUDE",
                            color_discrete_sequence=[color],
                            size='INCIDENCE',
                            height=500,
                            width=704,
                            zoom=12,
                            mapbox_style=theme)
    fig.update_layout(margin={
        'r': 0,
        't': 0,
        'l': 0,
        'b': 0
    })
    return fig


# @st.cache(show_spinner=False)
def distplot(data: DataFrame or list, title: str, theme='dark', color='#6717AD') -> Figure:
    """
    A distplot of RESIDUAL values

    :param data: A DataFrame with RESIDUAL column
    :param title: text will displayed in title figure
    :param theme: theme of background graph (default is 'carto-darkmatter')
    :param color: color of dist bars (default is '#6717AD')
    :return: Figure of graph plotted
    """

    # data = DataFrame(data, columns=['LABEL', 'RESIDUAL'])

    face_color = '#202020'
    tick_color = '#ffffff'

    if theme != 'carto-darkmatter':
        face_color = '#ffffff'
        tick_color = '#202020'

    sns.set(rc={
        'axes.facecolor': face_color,
        'figure.facecolor': face_color,
        'axes.labelcolor': face_color,
        'xtick.color': tick_color,
        'ytick.color': tick_color,
        'grid.linestyle': ''
    })

    fig = sns.displot(
        data['RESIDUAL'],
        kde=True,
        color=color,
        height=6,
        aspect=1.5).set_titles(title)

    return fig.figure


def reg_plot(data: DataFrame or list, label="LATITUDE", title="", theme='dark', color='#6717AD') -> Figure:
    """
    A distplot of RESIDUAL values

    :param label: Name of label ('LATITUDE' or 'LONGITUDE')
    :param data: A DataFrame with RESIDUAL column
    :param title: text will displayed in title figure
    :param theme: theme of background graph (default is 'carto-darkmatter')
    :param color: color of dist bars (default is '#6717AD')
    :return: Figure of graph plotted
    """

    # data = DataFrame(data, columns=['LABEL', 'RESIDUAL'])

    face_color = '#202020'
    tick_color = '#ffffff'

    if theme != 'carto-darkmatter':
        face_color = '#ffffff'
        tick_color = '#202020'

    sns.set(rc={
        'axes.facecolor': face_color,
        'figure.facecolor': face_color,
        'axes.labelcolor': face_color,
        'xtick.color': tick_color,
        'ytick.color': tick_color,
        'grid.linestyle': ''
    })

    fig = sns.regplot(
        x=label,
        y='RESIDUAL',
        data=data,
        scatter_kws={'color': '#6717AD', 'edgecolor': 'white'},
        line_kws={'color': color, 'lw': 5}) #.set_titles(title)

    return fig.figure
