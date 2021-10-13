"""
Home page settings, render and config

> home_render - Render the home page
"""
import collections

import streamlit as st
from App.Pages.Components.map import scatterplot_map, heat_map, bubble_map, distplot
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
                                   value='#DC2F02')
        _secondary = st.color_picker(label='Secondary color',
                                     value='#7D28C9')
        st.markdown('---')
        _is_real = st.checkbox(label='Show real values',
                               value=False,
                               help='Display real values in addition to predicted')
        st.text(' ')

    # Model settings section
    with st.sidebar.expander('⚙️ Model'):
        st.caption('Settings of IA model')
        st.markdown('---')
        _streetor_ia = st.checkbox(label='Streetor IA ℠',
                                   value=True)
        if not _streetor_ia:
            st.text(' ')
            col, _ = st.columns([1.6, 0.1])
            _clusters = col.select_slider(label='Number of Clusters',
                                          options=range(0, 250),
                                          value=0)
            _k = col.select_slider(label='K value',
                                   options=range(1, 6),
                                   value=1)
            _acc = col.slider(label='Accuracy level',
                              min_value=0.0,
                              max_value=2.0,
                              value=1.5,
                              step=0.1,
                              format='%f KM')
        else:
            _clusters = 0
            _k = 1
            _acc = 1
            st.text(' ')

    with st.sidebar.expander('💾 Database'):
        st.caption('Settings and Visualization Data')
        st.markdown('---')
        st.markdown('<b>Options</b>', unsafe_allow_html=True)
        _fatal_only = st.checkbox(label='Only fatality accidents',
                                  value=False)
        _street_only = st.checkbox(label='Only streets',
                                   value=False)
        _show_address = st.checkbox(label='Show address',
                                    value=False,
                                    help='This requires a very high cost, so it may take a while')
        st.markdown('---')
        _city = st.selectbox('City', ['ADAMANTINA', 'ADOLFO', 'AGUAI', 'AGUAS DA PRATA',
           'AGUAS DE LINDOIA', 'AGUAS DE SANTA BARBARA', 'AGUAS DE SAO PEDRO',
           'AGUDOS', 'ALAMBARI', 'ALFREDO MARCONDES', 'ALTAIR', 'ALTINOPOLIS',
           'ALTO ALEGRE', 'ALUMINIO', 'ALVARES FLORENCE', 'ALVARES MACHADO',
           'ALVARO DE CARVALHO', 'ALVINLANDIA', 'AMERICANA',
           'AMERICO BRASILIENSE', 'AMERICO DE CAMPOS', 'AMPARO', 'ANALANDIA',
           'ANDRADINA', 'ANGATUBA', 'ANHEMBI', 'ANHUMAS', 'APARECIDA',
           'APARECIDA D OESTE', 'APIAI', 'ARACARIGUAMA', 'ARACATUBA',
           'ARACOIABA DA SERRA', 'ARAMINA', 'ARANDU', 'ARAPEI', 'ARARAQUARA',
           'ARARAS', 'ARCO-IRIS', 'AREALVA', 'AREIAS', 'AREIOPOLIS',
           'ARIRANHA', 'ARTUR NOGUEIRA', 'ARUJA', 'ASPASIA', 'ASSIS',
           'ATIBAIA', 'AURIFLAMA', 'AVAI', 'AVANHANDAVA', 'AVARE',
           'BADY BASSITT', 'BALBINOS', 'BALSAMO', 'BANANAL',
           'BARAO DE ANTONINA', 'BARBOSA', 'BARIRI', 'BARRA BONITA',
           'BARRA DO CHAPEU', 'BARRA DO TURVO', 'BARRETOS', 'BARRINHA',
           'BARUERI', 'BASTOS', 'BATATAIS', 'BAURU', 'BEBEDOURO',
           'BENTO DE ABREU', 'BERNARDINO DE CAMPOS', 'BERTIOGA', 'BILAC',
           'BIRIGUI', 'BIRITIBA MIRIM', 'BOA ESPERANCA DO SUL', 'BOCAINA',
           'BOFETE', 'BOITUVA', 'BOM JESUS DOS PERDOES',
           'BOM SUCESSO DE ITARARE', 'BORA', 'BORACEIA', 'BORBOREMA',
           'BOREBI', 'BOTUCATU', 'BRAGANCA PAULISTA', 'BRAUNA',
           'BREJO ALEGRE', 'BRODOWSKI', 'BROTAS', 'BURI', 'BURITAMA',
           'BURITIZAL', 'CABRALIA PAULISTA', 'CABREUVA', 'CACAPAVA',
           'CACHOEIRA PAULISTA', 'CACONDE', 'CAFELANDIA', 'CAIABU',
           'CAIEIRAS', 'CAIUA', 'CAJAMAR', 'CAJATI', 'CAJOBI', 'CAJURU',
           'CAMPINA DO MONTE ALEGRE', 'CAMPINAS', 'CAMPO LIMPO PAULISTA',
           'CAMPOS DO JORDAO', 'CAMPOS NOVOS PAULISTA', 'CANANEIA', 'CANAS',
           'CANDIDO MOTA', 'CANDIDO RODRIGUES', 'CANITAR', 'CAPAO BONITO',
           'CAPELA DO ALTO', 'CAPIVARI', 'CARAGUATATUBA', 'CARAPICUIBA',
           'CARDOSO', 'CASA BRANCA', 'CASSIA DOS COQUEIROS', 'CASTILHO',
           'CATANDUVA', 'CATIGUA', 'CEDRAL', 'CERQUEIRA CESAR', 'CERQUILHO',
           'CESARIO LANGE', 'CHARQUEADA', 'CHAVANTES', 'CLEMENTINA', 'COLINA',
           'COLOMBIA', 'CONCHAL', 'CONCHAS', 'CORDEIROPOLIS', 'COROADOS',
           'CORONEL MACEDO', 'CORUMBATAI', 'COSMOPOLIS', 'COSMORAMA', 'COTIA',
           'CRAVINHOS', 'CRISTAIS PAULISTA', 'CRUZALIA', 'CRUZEIRO',
           'CUBATAO', 'CUNHA', 'DESCALVADO', 'DIADEMA', 'DIRCE REIS',
           'DIVINOLANDIA', 'DOBRADA', 'DOIS CORREGOS', 'DOLCINOPOLIS',
           'DOURADO', 'DRACENA', 'DUARTINA', 'DUMONT', 'ECHAPORA', 'ELDORADO',
           'ELIAS FAUSTO', 'ELISIARIO', 'EMBAUBA', 'EMBU DAS ARTES',
           'EMBU-GUACU', 'EMILIANOPOLIS', 'ENGENHEIRO COELHO',
           'ESPIRITO SANTO DO PINHAL', 'ESPIRITO SANTO DO TURVO',
           'ESTIVA GERBI', 'ESTRELA D OESTE', 'ESTRELA DO NORTE',
           'EUCLIDES DA CUNHA PAULISTA', 'FARTURA', 'FERNANDO PRESTES',
           'FERNANDOPOLIS', 'FERNAO', 'FERRAZ DE VASCONCELOS', 'FLORA RICA',
           'FLOREAL', 'FLORIDA PAULISTA', 'FLORINEA', 'FRANCA',
           'FRANCISCO MORATO', 'FRANCO DA ROCHA', 'GABRIEL MONTEIRO', 'GALIA',
           'GARCA', 'GASTAO VIDIGAL', 'GAVIAO PEIXOTO', 'GENERAL SALGADO',
           'GETULINA', 'GLICERIO', 'GUAICARA', 'GUAIMBE', 'GUAIRA',
           'GUAPIACU', 'GUAPIARA', 'GUARA', 'GUARACAI', 'GUARACI', 'GUARANTA',
           'GUARARAPES', 'GUARAREMA', 'GUARATINGUETA', 'GUAREI', 'GUARIBA',
           'GUARUJA', 'GUARULHOS', 'GUATAPARA', 'GUZOLANDIA', 'HERCULANDIA',
           'HOLAMBRA', 'HORTOLANDIA', 'IACANGA', 'IACRI', 'IARAS', 'IBATE',
           'IBIRA', 'IBIRAREMA', 'IBITINGA', 'IBIUNA', 'ICEM', 'IEPE',
           'IGARACU DO TIETE', 'IGARAPAVA', 'IGARATA', 'IGUAPE',
           'ILHA COMPRIDA', 'ILHA SOLTEIRA', 'ILHABELA', 'INDAIATUBA',
           'INDIANA', 'INDIAPORA', 'INUBIA PAULISTA', 'IPAUSSU', 'IPERO',
           'IPEUNA', 'IPIGUA', 'IPORANGA', 'IPUA', 'IRACEMAPOLIS', 'IRAPUA',
           'IRAPURU', 'ITABERA', 'ITAI', 'ITAJOBI', 'ITAJU', 'ITANHAEM',
           'ITAOCA', 'ITAPECERICA DA SERRA', 'ITAPETININGA', 'ITAPEVA',
           'ITAPEVI', 'ITAPIRA', 'ITAPIRAPUA PAULISTA', 'ITAPOLIS',
           'ITAPORANGA', 'ITAPUI', 'ITAPURA', 'ITAQUAQUECETUBA', 'ITARARE',
           'ITARIRI', 'ITATIBA', 'ITATINGA', 'ITIRAPINA', 'ITIRAPUA', 'ITOBI',
           'ITU', 'ITUPEVA', 'ITUVERAVA', 'JABORANDI', 'JABOTICABAL',
           'JACAREI', 'JACI', 'JACUPIRANGA', 'JAGUARIUNA', 'JALES',
           'JAMBEIRO', 'JANDIRA', 'JARDINOPOLIS', 'JARINU', 'JAU',
           'JERIQUARA', 'JOANOPOLIS', 'JOAO RAMALHO', 'JOSE BONIFACIO',
           'JULIO MESQUITA', 'JUMIRIM', 'JUNDIAI', 'JUNQUEIROPOLIS', 'JUQUIA',
           'JUQUITIBA', 'LAGOINHA', 'LARANJAL PAULISTA', 'LAVINIA',
           'LAVRINHAS', 'LEME', 'LENCOIS PAULISTA', 'LIMEIRA', 'LINDOIA',
           'LINS', 'LORENA', 'LOURDES', 'LOUVEIRA', 'LUCELIA', 'LUCIANOPOLIS',
           'LUIS ANTONIO', 'LUIZIANIA', 'LUPERCIO', 'LUTECIA', 'MACATUBA',
           'MACAUBAL', 'MACEDONIA', 'MAGDA', 'MAIRINQUE', 'MAIRIPORA',
           'MANDURI', 'MARABA PAULISTA', 'MARACAI', 'MARAPOAMA', 'MARIAPOLIS',
           'MARILIA', 'MARINOPOLIS', 'MARTINOPOLIS', 'MATAO', 'MAUA',
           'MENDONCA', 'MERIDIANO', 'MESOPOLIS', 'MIGUELOPOLIS',
           'MINEIROS DO TIETE', 'MIRA ESTRELA', 'MIRACATU', 'MIRANDOPOLIS',
           'MIRANTE DO PARANAPANEMA', 'MIRASSOL', 'MIRASSOLANDIA', 'MOCOCA',
           'MOGI DAS CRUZES', 'MOGI GUACU', 'MOGI MIRIM', 'MOMBUCA',
           'MONCOES', 'MONGAGUA', 'MONTE ALEGRE DO SUL', 'MONTE ALTO',
           'MONTE APRAZIVEL', 'MONTE AZUL PAULISTA', 'MONTE CASTELO',
           'MONTE MOR', 'MONTEIRO LOBATO', 'MORRO AGUDO', 'MORUNGABA',
           'MOTUCA', 'MURUTINGA DO SUL', 'NANTES', 'NARANDIBA',
           'NATIVIDADE DA SERRA', 'NAZARE PAULISTA', 'NEVES PAULISTA',
           'NHANDEARA', 'NIPOA', 'NOVA ALIANCA', 'NOVA CAMPINA',
           'NOVA CANAA PAULISTA', 'NOVA CASTILHO', 'NOVA EUROPA',
           'NOVA GRANADA', 'NOVA GUATAPORANGA', 'NOVA INDEPENDENCIA',
           'NOVA LUZITANIA', 'NOVA ODESSA', 'NOVAIS', 'NOVO HORIZONTE',
           'NUPORANGA', 'OCAUCU', 'OLEO', 'OLIMPIA', 'ONDA VERDE', 'ORIENTE',
           'ORINDIUVA', 'ORLANDIA', 'OSASCO', 'OSCAR BRESSANE',
           'OSVALDO CRUZ', 'OURINHOS', 'OURO VERDE', 'OUROESTE', 'PACAEMBU',
           'PALESTINA', 'PALMARES PAULISTA', 'PALMEIRA D OESTE', 'PALMITAL',
           'PANORAMA', 'PARAGUACU PAULISTA', 'PARAIBUNA', 'PARAISO',
           'PARANAPANEMA', 'PARANAPUA', 'PARAPUA', 'PARDINHO',
           'PARIQUERA-ACU', 'PARISI', 'PATROCINIO PAULISTA', 'PAULICEIA',
           'PAULINIA', 'PAULISTANIA', 'PAULO DE FARIA', 'PEDERNEIRAS',
           'PEDRA BELA', 'PEDRANOPOLIS', 'PEDREGULHO', 'PEDREIRA',
           'PEDRINHAS PAULISTA', 'PEDRO DE TOLEDO', 'PENAPOLIS',
           'PEREIRA BARRETO', 'PEREIRAS', 'PERUIBE', 'PIACATU', 'PIEDADE',
           'PILAR DO SUL', 'PINDAMONHANGABA', 'PINDORAMA', 'PINHALZINHO',
           'PIQUEROBI', 'PIQUETE', 'PIRACAIA', 'PIRACICABA', 'PIRAJU',
           'PIRAJUI', 'PIRANGI', 'PIRAPORA DO BOM JESUS', 'PIRAPOZINHO',
           'PIRASSUNUNGA', 'PIRATININGA', 'PITANGUEIRAS', 'PLANALTO',
           'PLATINA', 'POA', 'POLONI', 'POMPEIA', 'PONGAI', 'PONTAL',
           'PONTALINDA', 'PONTES GESTAL', 'POPULINA', 'PORANGABA',
           'PORTO FELIZ', 'PORTO FERREIRA', 'POTIM', 'POTIRENDABA',
           'PRACINHA', 'PRADOPOLIS', 'PRAIA GRANDE', 'PRATANIA',
           'PRESIDENTE ALVES', 'PRESIDENTE BERNARDES', 'PRESIDENTE EPITACIO',
           'PRESIDENTE PRUDENTE', 'PRESIDENTE VENCESLAU', 'PROMISSAO',
           'QUADRA', 'QUATA', 'QUEIROZ', 'QUELUZ', 'QUINTANA', 'RAFARD',
           'RANCHARIA', 'REDENCAO DA SERRA', 'REGENTE FEIJO', 'REGINOPOLIS',
           'REGISTRO', 'RESTINGA', 'RIBEIRA', 'RIBEIRAO BONITO',
           'RIBEIRAO BRANCO', 'RIBEIRAO CORRENTE', 'RIBEIRAO DO SUL',
           'RIBEIRAO DOS INDIOS', 'RIBEIRAO GRANDE', 'RIBEIRAO PIRES',
           'RIBEIRAO PRETO', 'RIFAINA', 'RINCAO', 'RINOPOLIS', 'RIO CLARO',
           'RIO DAS PEDRAS', 'RIO GRANDE DA SERRA', 'RIOLANDIA', 'RIVERSUL',
           'ROSANA', 'ROSEIRA', 'RUBIACEA', 'RUBINEIA', 'SABINO', 'SAGRES',
           'SALES', 'SALES OLIVEIRA', 'SALESOPOLIS', 'SALMOURAO', 'SALTINHO',
           'SALTO', 'SALTO DE PIRAPORA', 'SALTO GRANDE', 'SANDOVALINA',
           'SANTA ADELIA', 'SANTA ALBERTINA', 'SANTA BARBARA D OESTE',
           'SANTA BRANCA', 'SANTA CLARA D OESTE', 'SANTA CRUZ DA CONCEICAO',
           'SANTA CRUZ DA ESPERANCA', 'SANTA CRUZ DAS PALMEIRAS',
           'SANTA CRUZ DO RIO PARDO', 'SANTA ERNESTINA', 'SANTA FE DO SUL',
           'SANTA GERTRUDES', 'SANTA ISABEL', 'SANTA LUCIA',
           'SANTA MARIA DA SERRA', 'SANTA MERCEDES', 'SANTA RITA D OESTE',
           'SANTA RITA DO PASSA QUATRO', 'SANTA ROSA DE VITERBO',
           'SANTA SALETE', 'SANTANA DA PONTE PENSA', 'SANTANA DE PARNAIBA',
           'SANTO ANASTACIO', 'SANTO ANDRE', 'SANTO ANTONIO DA ALEGRIA',
           'SANTO ANTONIO DE POSSE', 'SANTO ANTONIO DO ARACANGUA',
           'SANTO ANTONIO DO JARDIM', 'SANTO ANTONIO DO PINHAL',
           'SANTO EXPEDITO', 'SANTOPOLIS DO AGUAPEI', 'SANTOS',
           'SAO BENTO DO SAPUCAI', 'SAO BERNARDO DO CAMPO',
           'SAO CAETANO DO SUL', 'SAO CARLOS', 'SAO FRANCISCO',
           'SAO JOAO DA BOA VISTA', 'SAO JOAO DAS DUAS PONTES',
           'SAO JOAO DE IRACEMA', 'SAO JOAO DO PAU D ALHO',
           'SAO JOAQUIM DA BARRA', 'SAO JOSE DA BELA VISTA',
           'SAO JOSE DO BARREIRO', 'SAO JOSE DO RIO PARDO',
           'SAO JOSE DO RIO PRETO', 'SAO JOSE DOS CAMPOS',
           'SAO LOURENCO DA SERRA', 'SAO LUIS DO PARAITINGA', 'SAO MANUEL',
           'SAO MIGUEL ARCANJO', 'SAO PAULO', 'SAO PEDRO',
           'SAO PEDRO DO TURVO', 'SAO ROQUE', 'SAO SEBASTIAO',
           'SAO SEBASTIAO DA GRAMA', 'SAO SIMAO', 'SAO VICENTE', 'SARAPUI',
           'SARUTAIA', 'SEBASTIANOPOLIS DO SUL', 'SERRA AZUL', 'SERRA NEGRA',
           'SERRANA', 'SERTAOZINHO', 'SETE BARRAS', 'SEVERINIA', 'SILVEIRAS',
           'SOCORRO', 'SOROCABA', 'SUD MENNUCCI', 'SUMARE', 'SUZANAPOLIS',
           'SUZANO', 'TABAPUA', 'TABATINGA', 'TABOAO DA SERRA', 'TACIBA',
           'TAGUAI', 'TAIACU', 'TAIUVA', 'TAMBAU', 'TANABI', 'TAPIRAI',
           'TAPIRATIBA', 'TAQUARAL', 'TAQUARITINGA', 'TAQUARITUBA',
           'TAQUARIVAI', 'TARABAI', 'TARUMA', 'TATUI', 'TAUBATE', 'TEJUPA',
           'TEODORO SAMPAIO', 'TERRA ROXA', 'TIETE', 'TIMBURI',
           'TORRE DE PEDRA', 'TORRINHA', 'TRABIJU', 'TREMEMBE',
           'TRES FRONTEIRAS', 'TUIUTI', 'TUPA', 'TUPI PAULISTA', 'TURIUBA',
           'TURMALINA', 'UBARANA', 'UBATUBA', 'UBIRAJARA', 'UCHOA',
           'UNIAO PAULISTA', 'URANIA', 'URU', 'URUPES', 'VALENTIM GENTIL',
           'VALINHOS', 'VALPARAISO', 'VARGEM', 'VARGEM GRANDE DO SUL',
           'VARGEM GRANDE PAULISTA', 'VARZEA PAULISTA', 'VERA CRUZ',
           'VINHEDO', 'VIRADOURO', 'VISTA ALEGRE DO ALTO', 'VITORIA BRASIL',
           'VOTORANTIM', 'VOTUPORANGA', 'ZACARIAS'], index=465)
        st.write(' ')
        col, _ = st.columns([1.6, 0.1])
        _min_period, _max_period = col.slider(label='Period',
                                              min_value=2007,
                                              max_value=2021,
                                              value=(2010, 2021),
                                              step=1)
        st.write(' ')
        col_1, col_2 = st.columns([1, 1])
        _week = col_1.selectbox('Day of Week', [
            'MONDAY',
            'TUESDAY',
            'WEDNESDAY',
            'THURSDAY',
            'FRIDAY',
            'SATURDAY',
            'SUNDAY'
        ], index=4)
        _period_day = col_2.selectbox('Period of Day', [
            'MORNING',
            'AFTERNOON',
            'EVENING',
            'NIGHT'
        ], index=2)
        st.text(' ')

    _options = collections.defaultdict()
    _options['CITY'] = _city
    _options['WEEK'] = _week
    _options['PERIOD'] = _period_day
    if _street_only:
        _options['ROAD'] = 'STREET'
    if _fatal_only:
        _options['DEATH'] = 1
    _options['$and'] = [
        {
            'YEAR': {
                '$gte': _min_period
            }
        },
        {
            'YEAR': {
                '$lte': _max_period
            }
        }
    ]
    # st.write(_options)

    st.sidebar.markdown('---')
    if st.sidebar.button('⚡ API'):
        cookies.set('route', 'api')
        st.experimental_rerun()

    # MAIN PANEL

    model = load_model(
        fields={
            '_id': 0,
            'CITY': 0,
            'PLACE': 0,
            'WEEK': 0,
            'PERIOD': 0,
            'ROAD': 0,
            'VEHICLE': 0
        },
        filter=_options
    )
    data, infos = run_model(model=model,
                            knn=_k,
                            clusters=_clusters,
                            acc=_acc)

    st.title('Streetor 🚗')
    st.caption('The best way to deal with a problem')
    st.markdown('---')
    _show = st.selectbox(label='',
                         options=[
                             '🗺️ Map',
                             '📊 Graph'
                         ])
    if _show == '🗺️ Map':
        _plot = st.radio('', ['🟠 Scatter', '🔴 Heat', '🟣 Bubble'])
        with st.empty():
            load_component('App/Template/loading.html')
            if _plot == '🟠 Scatter':
                st.plotly_chart(scatterplot_map(info=data,
                                                theme=_theme,
                                                colors=[_primary, _secondary],
                                                show_real=_is_real,
                                                address=_show_address))
            elif _plot == '🔴 Heat':
                st.plotly_chart(heat_map(infos['CLUSTERS_MAP'], theme=_theme))
            else:
                st.plotly_chart(bubble_map(infos['CLUSTERS_MAP'], theme=_theme))
    else:
        _plot = st.radio('', ['📈 Latitude', '📉 Longitude'])
        with st.empty():
            load_component('App/Template/loading.html')
            if _plot == '📈 Latitude':
                print(infos['RES_LAT'])
                st.pyplot(distplot(infos['RES_LAT'], 'LATITUDE RESIDUAL'))
            else:
                st.pyplot(distplot(infos['RES_LON'], 'LONGITUDE RESIDUAL'))
    st.markdown('### Information')
    with st.expander('🎯 Result', expanded=False):
        st.markdown(f'''
            ---
            | Tag | Values |
            | ----- | ----- |
            | Accuracy | `{infos['ACC']}%` |
            | R² | `{infos['R2']}%` |
            | Mean Absolute Error | `{infos['MAE']}` |
            | Mean Squared Error | `{infos['MSE']}` |
            | Root Mean Squared Error | `{infos['RMSE']}` |
            | Mean Latitude | `{infos['MED_LAT']}` |
            | Mean Longitude | `{infos['MED_LON']}` |
            | Sum Latitude | `{infos['SUM_LAT']}` |
            | Sum Longitude | `{infos['SUM_LON']}` |
        ''')
        st.write(' ')

    with st.expander('🤖 Machine Learning', expanded=False):
        st.markdown(f'''
            ---
            | Tag | Values |
            | ----- | ----- |
            | K value of KNN | `{infos['KNN']}` |
            | Number of Clusters | `{infos['CLUSTERS']}` |
            | Distance Variance | `{infos['KM']} KM`|
            | Metric Distance | `Haversine` |
        ''')
        st.write(' ')

    with st.expander('💾 Data', expanded=False):
        st.markdown(f'''
            ---
            | Tag | Values |
            | ----- | ----- |
            | City | `{_city}` |
            | Period | `{infos['PERIOD']}` |
            | Day of Week | `{infos['WEEK']}` |
            | Total of Accidents | `{infos['TOTAL']}` |
        ''')
        st.write(' ')

    # st.json({
    #     "dia": 31,
    #     "mês": "dezembro",
    #     "ano": 2020,
    #     "dia_da_semana": "sabádo",
    #     "periodo": "noite",
    #     "cidade": "sao paulo",
    #     "endereço": "avenida noel nutels",
    #     "latitude": -23.855579136848,
    #     "longitude": -46.71506881720071,
    #     "veiculo": "automovel",
    #     "via": "rua",
    #     "vitimas": 1,
    #     "fatalidade": "sim",
    #     "hora": "22:30",
    # })
    #
    # st.pyplot(distplot(DataFrame(infos['RES_LON']), 'Longitude Residual'))
