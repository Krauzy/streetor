"""
Access MongoDB module with pymongo
"""

import streamlit as st
import certifi
from pandas import DataFrame
from pymongo import MongoClient
from App.config import get_url


def get_collection(cluster='main', collection='accidents'):
    """
    Private function to get the collection of dataset

    :param cluster: Name of mongo cluster
    :param collection: Name of mongo collection inside the mongo cluster
    :return: Collection instance
    """

    client = MongoClient(get_url(), tlsCAFile=certifi.where())
    database = client[cluster]
    return database[collection]


@st.cache(show_spinner=False)
def get(fields=None, options=None, limit=5000, template='Dataframe') -> DataFrame or list:
    """
    Get function of MongoClient (similar to SELECT in SQL)

    :param fields: dict of fields selected (value = 1) or not selected (value = 0)
    :param options: dict of option values
    :param limit: Max documents to get
    :param template: 'DataFrame' or 'list'
    :return: DataFrame or list defined in template param
    """

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

    return list(cursor)
