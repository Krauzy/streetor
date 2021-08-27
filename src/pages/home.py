import streamlit as st
import plotly.express as px
from time import strftime, localtime
from datetime import datetime
from src.data.dataReader import get_dataset
from src.util.adaptalize import get_weekday
import src.pages.components as cmp

global global_theme, global_color_point


st.cache()
def get_map():
    df = get_dataset()
    fig = px.scatter_mapbox(df, 
                lat="Latitude", 
                lon="Longitude",
                color_discrete_sequence=['#6411ad'],
                # color='Type',
                hover_name='Vehicle',
                hover_data=['Victim', 'Day of Week', 'Hour'],
                height=500,
                zoom=10,
                mapbox_style="carto-darkmatter")
    fig.update_layout(margin={'r': 0, 't': 0, 'l': 0, 'b': 0})
    return fig
    
def render_home():
    st.set_page_config(
        page_title='Streetor',
        page_icon='🚗',
        layout='centered',
        initial_sidebar_state='collapsed'
    )
    cmp.set_radio_horizontal()
    static_week = strftime('%A', localtime())
    # Sidebar
    st.sidebar.title('🔧 Configurações')
    st.sidebar.markdown('---')
    with st.sidebar.expander('🗺️ Mapa'):
        st.markdown('---')
        global_theme = st.selectbox(label='Cor de Fundo', options=['Dark', 'Light', 'Padrão'], index=0)
        if global_theme == 'Dark':
            global_theme = 'carto-darkmatter'
        elif global_theme == 'Light':
            global_theme = 'carto-positron'
        else:
            global_theme = 'open-street-map'
        global_color_point = st.color_picker(label='Cor dos Pontos', value='#7D28C9')

    with st.sidebar.expander('⚙️ Modelo'):
        st.markdown('---')
        global_clusters = st.select_slider(label='Número de Clusters', options=range(1, 251), value=100)
        if global_clusters < 20:
            st.warning('Quantidade muito baixa de clusters')
        elif global_clusters > 150:
            st.warning('Quantidade muito alta de clusters')
        st.select_slider(label='Valor do K', options=range(1, 6), value=1,
                        help='O valor usado na regressão calculando a média dos K valores mais próximos')
    with st.sidebar.expander('📈 Predição'):
        st.markdown('---')
        global_now = st.checkbox(label='Predição de Agora',
                                help=get_weekday(static_week) + strftime(' - %H:%M', localtime()), value=True)
        if not global_now:
            st.selectbox(label='Dia da Predição',
                        options=['Segunda-Feira', 'Terça-Feira', 'Quarta-Feira', 'Quinta-Feira', 'Sexta-Feira', 'Sábado',
                                'Domingo'], index=get_weekday(static_week, True))
            st.time_input(label='Hora da Predição', value=datetime.now())
        st.markdown('---')
        st.write('Opções:')

    # with st.sidebar.beta_expander('💾 Base de Dados'):
    #     st.markdown('---')
    #     st.button('📂 Upload de dataset')
    #     st.write('-OU-')
    #     st.button('⚡ Inserir manualmente')

    st.sidebar.button('⌛ Recarregar')

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
        st.warning('Loading...')
        st.plotly_chart(get_map())
    with st.expander('❗️ Informações'):
        op_list = st.radio('', ['Lista', 'JSON'])
        st.write(' ')
        if op_list != 'JSON':
            st.code('Cidade: São Paulo'
                    + '\nAcidentes Registrados: 1000'
                    + '\nAcidentes Previstos: 489'
                    + '\nPrecisão de Predição: 93.75%',
                    language='')
            st.write(' ')
        else:
            st.json({
                'cidade': 'São Paulo',
                'acidentes_reg': '1000',
                'acidentes_prev': '489',
                'precisao': '93.75%'
            })
