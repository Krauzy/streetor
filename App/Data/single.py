from App.Data.streetor import StreetorModel
from pandas import DataFrame
from App.Database.db import get
import streamlit as st


@st.cache(show_spinner=False)
def load_model(fields, filter) -> StreetorModel:
    return StreetorModel(get(fields, filter, 5000))


@st.cache(show_spinner=False)
def run_model(model: StreetorModel, knn=1, clusters=100, acc=1.5) -> tuple:
    model.run(knn, clusters, acc)
    return model.response()




