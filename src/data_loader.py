import pandas as pd
import streamlit as st


# [IA] Gemini (streamlit skills) – estrutura de leitura com cache (@st.cache_data)
@st.cache_data
def load_data(path="data/clean/dataset.csv"):
    """Lê o dataset já tratado (exportado ao final do notebook de EDA)."""
    return pd.read_csv(path)
