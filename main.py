import pandas as pd
import streamlit as st
import plotly.express as px
from sklearn.cluster import KMeans


def plot_map(mapbox_style='carto-positron', period='Dawn', src_color='black', pred_color='red'):
    kmeans = KMeans(40)
    sp = pd.read_excel('./resources/dataset.xlsx')
    sp = sp[sp['Period'] == period]
    #print(kmeans)
    sp['cluster'] = kmeans.fit_predict(sp[['Latitude','Longitude']])
    fig = px.scatter_mapbox(sp,
                            lat='Latitude',
                            lon='Longitude',
                            hover_name='City',
                            hover_data=['Victim', 'Hour'],
                            color_discrete_sequence=[src_color, pred_color],
                            zoom=9,
                            height=500,
                            color='cluster')
    fig.update_layout(mapbox_style=mapbox_style)
    fig.update_layout(margin={'r': 0, 't': 0, 'l': 0, 'b': 0})
    fig.update_traces(mode='markers', marker=dict(size=8))
    st.plotly_chart(fig)


def break_lines(lines=1):
    for line in range(lines):
        st.text(' ')


def init():
    st.title('Streetor')
    st.write('Prevendo acidentes')
    break_lines(2)
    period = st.select_slider(label='Período',
                              options=['Manhã', 'Tarde', 'Noite', 'Madrugada'])
    if period == 'Manhã':
        period = 'Morning'
    elif period == 'Tarde':
        period = 'Afternoon'
    elif period == 'Noite':
        period = 'Night'
    else:
        period = 'Dawn'
    st.sidebar.title('Settings')
    op = st.sidebar.selectbox(label='Tema', options=['Open Street', 'Light', 'Dark'])
    side1, side2 = st.sidebar.beta_columns([1, 1])
    c = side1.color_picker(label='Pontos Originais:', value='#000000')
    color_pred = side2.color_picker(label='Pontos Preditivos:', value='#F15656')
    break_lines()
    st.radio(label='Distância Métrica:', options=['Euclidean', 'Manhattan', 'Chebyshev'])
    break_lines(2)
    if op == 'Default':
        plot_map(period=period, src_color=c, pred_color=color_pred)
    elif op == 'Dark':
        plot_map(mapbox_style='carto-darkmatter', period=period, src_color=c, pred_color=color_pred)
    else:
        plot_map(mapbox_style='open-street-map', period=period, src_color=c, pred_color=color_pred)

        
init()
