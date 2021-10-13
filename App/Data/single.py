"""
single request from StreamlitModel in cache
"""

import streamlit as st
from App.Data.streetor import StreetorModel
from App.Database.db import get


@st.cache(show_spinner=False, allow_output_mutation=True)
def load_model(fields: dict, filter: dict) -> StreetorModel:
    """
    Init the StreetorModel with *fields* and *filter* of dataset

    :param fields: A dict of fields that will be set in dataset
    :param filter: A dict of the filter that will be set in dataset
    :return: A StreetorModel instance
    """

    model = StreetorModel(get(fields, filter, 5000))
    model.week = filter['WEEK']
    model.period = filter['PERIOD']
    return model


@st.cache(show_spinner=False, allow_output_mutation=True)
def run_model(model: StreetorModel, knn=1, clusters=200, acc=0.5) -> tuple or None:
    """
    Running functions of *StreetorModel*

    :param model: A instance of StreetorModel
    :param knn: Number of K set by KNN
    :param clusters: Number of cluster set by KMeans
    :param acc: Accuracy metric value of Machine Learning model
    :return: If there is an error return is None, if not, return a tuple with
    predict dataset and a dict of stats
    """

    if model.error:
        st.error('Failed to load dataset')
        return None

    model.run(knn, clusters, acc)
    return model.response()
