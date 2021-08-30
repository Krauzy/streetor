from plotly.missing_ipywidgets import FigureWidget
import streamlit as st
import plotly.express as px
from time import strftime, localtime
from datetime import datetime
# from src.data.dataReader import get_dataset
from src.util.adaptalize import get_weekday, get_theme, get_weekday_revert
import src.pages.components as cmp
from src.data.analysis import Analysis

global global_theme, global_color_point_real, global_color_point_predict, global_info, global_acc, global_k, global_clusters, global_day, global_hour

st.cache()
def get_plot(data, n_clusters, k, acc, hour, day):
    shape = Analysis(data=data, n_clusters=n_clusters, k=k, acc=acc, hour=hour, day=day)
    shape.run()
    shape.plot()
    return shape.get_attribute()

st.cache()
def get_map(df, dis_color=['#DC2F02', '#7D28C9'], theme='open-street-map') -> FigureWidget:
    fig = px.scatter_mapbox(df, 
                lat="Latitude", 
                lon="Longitude",
                color_discrete_sequence=dis_color,
                color='Target',
                hover_name='Target',
                # hover_data=['Victim', 'Day of Week', 'Hour', 'Year'],
                height=500,
                width=810,
                zoom=10,
                mapbox_style=theme)
    fig.update_layout(margin={'r': 0, 't': 0, 'l': 0, 'b': 0})
    return fig


def render() -> None:
    st.set_page_config(
        page_title='Streetor',
        page_icon='🚗',
        layout='centered',
        initial_sidebar_state='collapsed'
    )

    cmp.set_radio_horizontal()
    static_week = strftime('%A', localtime())
    
    # ------------------------------------------------------------------------------
    # Sidebar
    st.sidebar.title('🔧 Configurações')
    st.sidebar.markdown('---')

    with st.sidebar.expander('🗺️ Mapa'):
        st.markdown('---')
        global_theme = get_theme(st.selectbox(label='Cor de Fundo', options=['Escuro', 'Claro', 'Padrão'], index=0))
        global_color_point_real = st.color_picker(label='Cor dos Locais Reais', value='#7D28C9')
        global_color_point_predict = st.color_picker(label='Cor dos Locais Preditos', value='#DC2F02')

    with st.sidebar.expander('⚙️ Modelo'):
        st.markdown('---')
        global_clusters = st.select_slider(label='Número de Clusters', options=range(0, 251), value=100)
        
        if global_clusters < 20 and global_clusters != 0:
            st.warning('Quantidade muito baixa de clusters')
        elif global_clusters > 150:
            st.warning('Quantidade muito alta de clusters')
        elif global_clusters == 0:
            st.warning('Quantidade de clusters será calculada pelo sistema')

        global_k = st.select_slider(label='Valor do K', 
                    options=range(1, 6), 
                    value=1,
                    help='O valor usado na regressão calculando a média dos K valores mais próximos')
        
    with st.sidebar.expander('📈 Predição'):
        st.markdown('---')
        temp_h = strftime('%H:%M', localtime())
        global_acc = st.select_slider(label='Predição de área (KM²)', value=15, options=range(0, 51), format_func=lambda x: x / 10) / 10
        global_now = st.checkbox(label='Predição de Agora',
                                help=get_weekday(static_week) + ' - ' + temp_h, 
                                value=False)
        if not global_now:
            global_geral = st.checkbox(label='Predição Total', value=True)
            if not global_geral:
                global_day = get_weekday_revert(st.selectbox(label='Dia da Predição',
                            options=[
                                'Segunda-Feira', 
                                'Terça-Feira', 
                                'Quarta-Feira', 
                                'Quinta-Feira', 
                                'Sexta-Feira', 
                                'Sábado', 
                                'Domingo'],
                            index=get_weekday(static_week, True)))
                global_hour = st.time_input(label='Hora da Predição', value=datetime.now())
            else:
                global_day = 'Geral'
                global_hour = 'Geral'
        else:
            global_day = static_week
            global_hour = temp_h
        st.write(' ')
        
    # with st.sidebar.expander('💾 Base de Dados'):
    #     st.markdown('---')
    #     st.file_uploader('Selecione o Arquivo', type=['csv', 'xlsx'])
    #     st.button('⚡ Carregar Dataset')

    # -------------------------------------------------------------------------------
    # Page
    st.title('Streetor 🚗')
    st.caption('O melhor jeito de lidar com um problema, é impedi-lo de acontecer')
    st.markdown('---')
    global_show = st.selectbox('Exibir', options=['🗺️ Mapa', '📊 Gráfico'])
    arr_op = []
    
    if global_show == '🗺️ Mapa':
        arr_op = ['Locais Preditos', 'Regiões Preditas', 'Perigo Eminente']
    else:
        arr_op = ['Resíduos', 'Amostragem', 'Clustering']

    st.radio(label='', options=arr_op)
    with st.empty():
        st.warning('⌛ Loading...')        
        data, global_info = get_plot(
            data=None, 
            n_clusters=global_clusters, 
            k=global_k, 
            hour=global_hour, 
            day=global_day,
            acc=global_acc)
        st.plotly_chart(get_map(data,
                dis_color=[global_color_point_predict, global_color_point_real],
                theme=global_theme))
    
    with st.expander('❗️ Informações'):
        op_list = st.radio('', ['Lista', 'JSON'])
        st.write(' ')
        if op_list != 'JSON':
            st.code('Cidade: São Paulo'
                    + '\nAcidentes Registrados: ' + str(global_info['TOTAL'])
                    + '\nAcidentes Previstos: ' + str(len(data[data['Target'] == 'predict']))
                    + '\nPrecisão de Predição: ' + str(global_info['ACC']) + '%'
                    + '\nMédia Absoluta do Erro: ' + str(global_info['MAE'])
                    + '\nMédia Quadrática do Erro: ' + str(global_info['MSE'])
                    + '\nCoeficiente de Determinação: ' + str(global_info['R2']) + '%'
                    + '\nMédia Residual da Latitude: ' + str(global_info['M_LATITUDE'])
                    + '\nMédia Residual da Longitude: ' + str(global_info['M_LONGITUDE'])
                    + '\nMédia Residual da Latitude: ' + str(global_info['M_LATITUDE'])
                    + '\nSoma Residual da Latitude: ' + str(global_info['S_LATITUDE'])
                    + '\nSoma Residual da Longitude: ' + str(global_info['S_LONGITUDE']),
                    language='')
        else:
            st.json({
                'cidade': 'São Paulo',
                'acidentes_reg': '1000',
                'acidentes_prev': '489',
                'precisao': '93.75%'
            })
        st.write(' ')
