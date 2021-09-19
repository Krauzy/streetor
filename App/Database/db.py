from pymongo import MongoClient
from App.config import get_url
import streamlit as st
from pandas import DataFrame


def get_collection(cluster='main', collection='accidents'):
    client = MongoClient(get_url())
    db = client[cluster]
    return db[collection]


@st.cache(show_spinner=False)
def get(fields=None, options=None, limit=5, template='Dataframe') -> DataFrame or list:
    if options is None:
        options = {}
    if fields is None:
        fields = {}

    if (template != 'Dataframe') | (template != 'List'):
        template = 'List'

    collection = get_collection()
    cursor = collection.find(options,
                             fields,
                             limit=limit)

    if template == 'Dataframe':
        return DataFrame(list(cursor))
    else:
        return list(cursor)
