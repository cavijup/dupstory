import streamlit as st
from google_connection import load_data
from graficos.grafico_dub import crear_grafico_dub
from graficos.grafico_fechas import crear_grafico_fechas
from utils.image_utils import mostrar_imagen_drive  # Importar la función

def mostrar_pagina_dub():
    """
    Muestra el contenido de la pestaña DUB con la imagen de Google Drive
    y la nueva estructura de gráficos.
    """
    st.header("Datos DUB")
    
    # Mostrar la imagen de Google Drive en la parte superior
    # Puedes ajustar el valor de width según necesites
    file_id = "1J_E2c8zuNxaJ5zguZG6oagzvWknPLncS"
    
    # Crear tres columnas para centrar la imagen
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        # Mostrar la imagen en la columna central para que aparezca centrada
        mostrar_imagen_drive(file_id, width=400)
    
    # Mostrar un spinner mientras cargamos los datos
    with st.spinner("Cargando datos desde Google Sheets..."):
        try:
            # Cargar los datos desde la hoja "DUB"
            sheet_id = "16jdYbgDidCSxYv3JRzWgmM2POxUn9cw6xVRYmfSMqhU"
            df = load_data(sheet_id, "DUB")
            
            if df is not None and not df.empty:
                # Mostrar información básica
                st.success(f"Datos cargados correctamente. Total de filas: {len(df)}")
                
                # 1. BARRA HORIZONTAL DE PROGRESO ID DUB (en la primera fila, ancho completo)
                crear_grafico_dub(df)
                
                # Separador visual
                st.markdown("---")
                
                # 2. GRÁFICO DE BARRAS DE FECHA (debajo de la barra de progreso)
                crear_grafico_fechas(df)
                
                # 3. MUESTRA DE DATOS EXPANDIBLE
                with st.expander("Ver muestra de datos"):
                    st.dataframe(df.head(10), use_container_width=True)
                
            else:
                st.error("No se pudieron cargar los datos.")
        except Exception as e:
            st.error(f"Error en la aplicación: {e}")