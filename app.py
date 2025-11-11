import streamlit as st
import pandas as pd
import plotly.express as px

# Título de la app
st.title("📊 Análisis de Extorsiones en Colombia 2025")

# Cargar el conjunto de datos
df = pd.read_csv("Extorsiones-2025.csv")

# Mostrar los primeros registros
st.subheader("Vista previa del conjunto de datos")
st.dataframe(df.head())
