import streamlit as st
import pandas as pd
import plotly.express as px
import os

# Configuración de la página
st.set_page_config(page_title="Análisis de Extorsiones", layout="wide")
st.title("📊 Análisis de Extorsiones en Colombia 2025")

# Función para cargar datos usando ruta relativa
@st.cache_data
def cargar_datos():
    csv_path = os.path.join("data", "Extorsiones-2025.csv")  # Ruta relativa
    if not os.path.exists(csv_path):
        st.error(f"Archivo no encontrado en: {csv_path}")
        return None
    df = pd.read_csv(csv_path)
    return df

# Cargar CSV
df = cargar_datos()

if df is not None:
    # Dividir en dos columnas
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Top 10 Departamentos")
        if "DEPARTAMENTO" in df.columns and "CANTIDAD" in df.columns:
            top10_depart = (
                df.groupby("DEPARTAMENTO")["CANTIDAD"]
                .sum()
                .reset_index()
                .sort_values(by="CANTIDAD", ascending=False)
                .head(10)
            )
            fig_pie_dep = px.pie(
                top10_depart,
                names="DEPARTAMENTO",
                values="CANTIDAD",
                title="Departamentos con mayor número de extorsiones",
                color_discrete_sequence=px.colors.qualitative.Set3,
                hole=0.4
            )
            fig_pie_dep.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig_pie_dep, use_container_width=True)
        else:
            st.warning("⚠️ No se encontraron las columnas 'DEPARTAMENTO' o 'CANTIDAD' en el dataset.")

    with col2:
        st.subheader("Top 10 Municipios")
        if "MUNICIPIO" in df.columns and "CANTIDAD" in df.columns:
            top10_muni = (
                df.groupby("MUNICIPIO")["CANTIDAD"]
                .sum()
                .reset_index()
                .sort_values(by="CANTIDAD", ascending=False)
                .head(10)
            )
            fig_pie_muni = px.pie(
                top10_muni,
                names="MUNICIPIO",
                values="CANTIDAD",
                title="Municipios con mayor número de extorsiones",
                color_discrete_sequence=px.colors.qualitative.Pastel,
                hole=0.4
            )
            fig_pie_muni.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig_pie_muni, use_container_width=True)
        else:
            st.warning("⚠️ No se encontraron las columnas 'MUNICIPIO' o 'CANTIDAD' en el dataset.")

    # Extorsiones por departamento
    st.header("🏢 Extorsiones por departamento")
    if "DEPARTAMENTO" in df.columns and "CANTIDAD" in df.columns:
        casos_por_departamento = df.groupby("DEPARTAMENTO")["CANTIDAD"].sum().reset_index()
        fig_bar = px.bar(
            casos_por_departamento,
            x="DEPARTAMENTO",
            y="CANTIDAD",
            color="DEPARTAMENTO",
            title="Casos de extorsión por departamento (2025)",
            text="CANTIDAD",
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        fig_bar.update_layout(
            xaxis={'categoryorder': 'total descending'},
            showlegend=False
        )
        st.plotly_chart(fig_bar, use_container_width=True)
    else:
        st.warning("⚠️ No se encontraron las columnas 'DEPARTAMENTO' o 'CANTIDAD' en el dataset.")

    # 30 municipios con mayor cantidad de casos
    st.header("💥 30 municipios con mayor cantidad de casos de extorsión")
    if "MUNICIPIO" in df.columns and "CANTIDAD" in df.columns:
        df_burbujas = (
            df.groupby("MUNICIPIO")["CANTIDAD"]
            .sum()
            .reset_index()
            .sort_values(by="CANTIDAD", ascending=False)
            .head(30)
        )
        fig_bubbles = px.scatter(
            df_burbujas,
            x="MUNICIPIO",
            y="CANTIDAD",
            size="CANTIDAD",
            color="CANTIDAD",
            color_continuous_scale="Turbo",
            size_max=60,
            hover_name="MUNICIPIO"
        )
        fig_bubbles.update_traces(marker=dict(opacity=0.8, line=dict(width=1, color="DarkSlateGrey")))
        fig_bubbles.update_layout(
            xaxis=dict(showgrid=False, title="Municipio", tickangle=-45),
            yaxis_title="Cantidad de casos",
            plot_bgcolor="white",
            paper_bgcolor="white"
        )
        st.plotly_chart(fig_bubbles, use_container_width=True)
    else:
        st.warning("⚠️ No se encontraron las columnas 'MUNICIPIO' o 'CANTIDAD' en el dataset.")

else:
    st.write("No se pudieron cargar los datos. Verifica que el archivo CSV esté en la carpeta 'data'.")
