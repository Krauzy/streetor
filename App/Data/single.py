from App.Data.streetor import StreetorModel
from App.Database.db import get
import streamlit as st


@st.cache(show_spinner=False, allow_output_mutation=True)
def load_model(fields, filter) -> StreetorModel:
    model = StreetorModel(get(fields, filter, 5000))
    model.week = filter['WEEK']
    model.period = filter['PERIOD']
    return model


@st.cache(show_spinner=False)
def run_model(model: StreetorModel, knn=1, clusters=200, acc=0.5) -> tuple or None:
    if model.error:
        st.error('Failed to load dataset')
        return None
    else:
        model.run(knn, clusters, acc)
        return model.response()




