from App.Data.streetor import StreetorModel
from pandas import DataFrame
import streamlit as st


@st.cache(show_spinner=False)
def load_model(data: DataFrame, filter: dict) -> StreetorModel:
    streetor = StreetorModel(data)
    if not streetor.error:
        p_week = filter['week'] if 'week' in filter else None
        p_period = filter['period'] if 'period' in filter else None
        streetor.filter(p_week, p_period)
        return streetor


@st.cache(show_spinner=False)
def run_model(model: StreetorModel, knn=1, clusters=100, acc=1.5) -> tuple:
    model.run(knn, clusters, acc)
    return model.response()




