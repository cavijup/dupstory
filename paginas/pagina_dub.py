import streamlit as st
from google_connection import load_data
from graficos.grafico_dub import crear_grafico_dub
from graficos.grafico_fechas import crear_grafico_fechas
from utils.svg_utils import mostrar_estadisticas_sexo
from graficos.graficos_adicionales import crear_grafico_pastel, crear_grafico_barras_horizontal, mostrar_graficos_pastel, mostrar_matriz_graficos_barras


def mostrar_pagina_dub():
    """
    Muestra el contenido de la pestaña DUB sin la imagen principal,
    solo con los gráficos y visualizaciones.
    """
    st.header("Datos DUB")
    
    # Mostrar un spinner mientras cargamos los datos
    with st.spinner("Cargando datos desde Google Sheets..."):
        try:
            # Cargar los datos desde la hoja "DUB"
            sheet_id = "16jdYbgDidCSxYv3JRzWgmM2POxUn9cw6xVRYmfSMqhU"
            df = load_data(sheet_id, "DUB")
            
            if df is not None and not df.empty:
                # Mostrar información básica
                st.success(f"Datos cargados correctamente. Total de filas: {len(df)}")
                
                # 1. PRIMERA FILA: BARRA HORIZONTAL DE PROGRESO ID DUB
                st.markdown("### Primera Fila: Progreso General")
                crear_grafico_dub(df)
                
                # Separador visual
                st.markdown("---")
                
                # 2. SEGUNDA FILA: GRÁFICO DE BARRAS DE FECHA
                st.markdown("### Segunda Fila: Análisis Temporal")
                crear_grafico_fechas(df)
                
                # Separador visual
                st.markdown("---")
                
                # 3. TERCERA FILA: MUESTRA DE DATOS EXPANDIBLE
                st.markdown("### Tercera Fila: Datos Crudos")
                with st.expander("Ver muestra de datos"):
                    st.dataframe(df.head(10), use_container_width=True)
                
                # Separador visual
                st.markdown("---")
                
                # 4. CUARTA FILA: VISUALIZACIÓN DE ESTADÍSTICAS POR SEXO
                st.markdown("### Cuarta Fila: Distribución Demográfica")
                
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
                
                # 5. QUINTA FILA: GRÁFICOS DE PASTEL PARA IDENTIDAD Y ORIENTACIÓN SEXUAL
                mostrar_graficos_pastel(df)
                
                # Separador visual
                st.markdown("---")
                
                # 6. SEXTA FILA: MATRIZ DE GRÁFICOS DE BARRAS
                mostrar_matriz_graficos_barras(df)
                
            else:
                st.error("No se pudieron cargar los datos.")
        except Exception as e:
            st.error(f"Error en la aplicación: {e}")