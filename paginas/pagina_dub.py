import streamlit as st
import pandas as pd
from utils.svg_utils import mostrar_estadisticas_sexo
from graficos.graficos_adicionales import crear_grafico_pastel, crear_grafico_barras_horizontal, mostrar_graficos_pastel, mostrar_matriz_graficos_barras
from google_connection import load_data


def mostrar_pagina_dub():
    """
    Muestra el contenido de la pestaña DUB con visualizaciones demográficas.
    
    Returns:
        DataFrame: Los datos cargados o None si hay un error
    """
    st.header("Demografía DUB")
    
    # Verificar si hay datos cargados en la sesión
    if 'df' in st.session_state:
        df = st.session_state.df
        st.success(f"Usando datos cargados. Total de filas: {len(df)}")
    else:
        # Si no hay datos cargados, intentar cargarlos
        with st.spinner("Cargando datos desde Google Sheets..."):
            try:
                # Cargar los datos desde la hoja "DUB"
                sheet_id = "19aYe071W4ktFUHOswLf9oB3nj2hcOvklavxdR8Ohv40"
                df = load_data(sheet_id, "DUB")
                
                if df is not None and not df.empty:
                    # Guardar en session_state para compartirlo entre pestañas
                    st.session_state.df = df
                    st.success(f"Datos cargados correctamente. Total de filas: {len(df)}")
                else:
                    st.error("No se pudieron cargar los datos.")
                    return None
            except Exception as e:
                st.error(f"Error en la aplicación: {e}")
                return None
    
    # 1. VISUALIZACIÓN DE ESTADÍSTICAS POR SEXO
    st.markdown("### Distribución Demográfica")
    
    # Verificar si existe la columna 'Sexo'
    if 'Sexo' not in df.columns:
        # Si no existe, intentamos buscar la columna AH
        try:
            # Renombramos la columna AH a 'Sexo' si existe
            columnas = list(df.columns)
            if len(columnas) >= 34:  # AH sería la columna 34 (0-indexado)
                df['Sexo'] = df[columnas[33]]  # AH sería la columna 34 (0-indexado)
            else:
                st.warning("No se encontró la columna en la posición AH. Por favor verifica la estructura de tus datos.")
        except Exception as e:
            st.warning(f"No se pudo acceder a la columna de Sexo: {e}")
    
    # Mostrar estadísticas de sexo con imágenes
    mostrar_estadisticas_sexo(df)
    
    # Separador visual
    st.markdown("---")
    
    # 2. GRÁFICOS DE PASTEL PARA IDENTIDAD Y ORIENTACIÓN SEXUAL
    mostrar_graficos_pastel(df)
    
    # Separador visual
    st.markdown("---")
    
    # 3. MATRIZ DE GRÁFICOS DE BARRAS
    mostrar_matriz_graficos_barras(df)
    
    # Devolver el DataFrame para que pueda ser usado en otras pestañas
    return df