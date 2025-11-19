import streamlit as st
import pandas as pd
import plotly.express as px
import os

# --- Configuración de la página ---
st.set_page_config(page_title="Análisis de Extorsiones", layout="wide")
st.title("📊 Análisis de Extorsiones en Colombia 2025")

# Paleta personalizada solicitada
COLORS = ["#780000", "#C1121F", "#FDF0D5", "#003049", "#669BBC"]

# --- Cargar datos desde ruta relativa ---
@st.cache_data
def cargar_datos():
    ruta = os.path.join("data", "Extorsiones-2025.csv")
    if not os.path.exists(ruta):
        st.error(f"Archivo no encontrado en: {ruta}")
        return None

    df = pd.read_csv(ruta)

    # Capitalizar nombres de departamentos y municipios
    if "DEPARTAMENTO" in df.columns:
        df["DEPARTAMENTO"] = df["DEPARTAMENTO"].str.title()

    if "MUNICIPIO" in df.columns:
        df["MUNICIPIO"] = df["MUNICIPIO"].str.title()

    return df


# Cargar datos
df = cargar_datos()

if df is not None:

    # --- Dividir pantalla en dos columnas ---
    col1, col2 = st.columns(2)

    # ===
