from pymongo import MongoClient
from App.config import get_url
import streamlit as st


@st.cache()
def get_connection():
    client = MongoClient(get_url())
    db = client['main']
    return db['accidents']


@st.cache()
def get():
    collection = get_connection()
    return collection.find()
