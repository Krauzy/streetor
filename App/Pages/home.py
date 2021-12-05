"""
Home page settings, render and config

> home_render - Render the home page
"""
import collections
import time
import streamlit as st
from App.Pages.Components.map import scatterplot_map, heat_map, bubble_map, distplot, reg_plot
from App.Pages.Components.load import load_component, load_style
from App.Data.single import load_model, run_model


def home_render() -> None:
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
            _force = col.checkbox(label="Force hard process", value=False)
        else:
            _clusters = 0
            _k = 1
            _acc = 0.5
            _force = False
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
        _city = st.selectbox('City', ['SAO PAULO', 'PRESIDENTE PRUDENTE'], index=0)
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

    # st.sidebar.markdown('---')
    # if st.sidebar.button('⚡ API'):
    #     cookies.set('route', 'api')
    #     st.experimental_rerun()

    # MAIN PANEL

    st.title('Streetor 🚗')
    st.caption('The best way to deal with a problem')
    st.markdown('---')
    _show = st.selectbox(label='',
                         options=[
                             '🗺️ Map',
                             '📊 Graph'
                         ])
    start = time.time_ns()
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
                            acc=_acc,
                            force=_force)
    stop = time.time_ns()

    if _show == '🗺️ Map':
        _plot = st.radio('', ['🟠 Scatter', '🔴 Heat', '🟣 Bubble'])
        with st.empty():
            st.spinner(text="Loading")
            # load_component('App/Template/loading.html')
            if _plot == '🟠 Scatter':
                st.plotly_chart(scatterplot_map(info=data,
                                                theme=_theme,
                                                colors=[_primary, _secondary],
                                                show_real=_is_real,
                                                address=_show_address))
            elif _plot == '🔴 Heat':
                st.plotly_chart(heat_map(infos['CLUSTERS_MAP'], theme=_theme))
            else:
                st.plotly_chart(bubble_map(infos['CLUSTERS_MAP'], theme=_theme, color=_primary))
    else:
        _plot = st.radio('', ['📈 Latitude', '📉 Longitude'])
        with st.empty():
            load_component('App/Template/loading.html')
            if _plot == '📈 Latitude':
                residual_index = 'RES_LAT'
                residual_label = 'LATITUDE'
            else:
                residual_index = 'RES_LON'
                residual_label = 'LONGITUDE'
            st.pyplot(reg_plot(data=infos[residual_index],
                               label=residual_label,
                               title='',
                               theme=_theme,
                               color=_primary))
    st.markdown('### Information')
    with st.expander('🎯 Result', expanded=False):
        st.markdown(f'''
            ---
            | Tag | Values |
            | ----- | ----- |
            | Accuracy | `{infos['ACC']}%` |
            | R² | `{infos['R2']}%` |
            | Error(m) | `{infos['ERROR'] * 1000}m`|
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
            | Runtime | `{round((stop - start) / 1000000, 1)} ms` |
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
