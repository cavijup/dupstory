import streamlit as st
import pandas as pd
import plotly.express as px
import os

def crear_grafico_pastel_con_imagen(df, columna, titulo, imagen_nombre, posicion_columna=None):
    """
    Crea un gráfico de pastel con una imagen relacionada arriba.
    
    Args:
        df: DataFrame con los datos
        columna: Nombre de la columna a mostrar
        titulo: Título a mostrar para el gráfico
        imagen_nombre: Nombre del archivo de imagen (sin extensión)
        posicion_columna: Índice de la columna si no se encuentra por nombre
    """
    # Intentar acceder a la columna por nombre o posición
    datos = None
    if columna in df.columns:
        datos = df[columna]
    elif posicion_columna is not None and len(df.columns) > posicion_columna:
        columnas = list(df.columns)
        datos = df[columnas[posicion_columna]]
        # Renombrar temporalmente para el gráfico
        df[columna] = datos
    
    if datos is None:
        st.warning(f"No se pudo encontrar la columna '{columna}' en los datos")
        return
    
    # Ruta de la imagen
    ruta_imagen = os.path.join("imagenes", f"{imagen_nombre}.png")
    
    # Mostrar imagen centrada
    st.image(ruta_imagen, width=100, use_column_width=False)
    
    # Mostrar título
    st.markdown(f"#### {titulo}")
    
    # Crear el conteo para el gráfico de pastel
    conteo = datos.value_counts()
    
    # Calcular porcentajes
    total = conteo.sum()
    porcentajes = (conteo / total * 100).round(1)
    
    # Crear etiquetas con porcentajes
    etiquetas = [f"{idx} ({val:.1f}%)" for idx, val in zip(conteo.index, porcentajes)]
    
    # Crear gráfico de pastel con Plotly
    fig = px.pie(
        values=conteo.values,
        names=etiquetas,
        title=f"Distribución de {titulo}",
        color_discrete_sequence=px.colors.qualitative.Set3,
    )
    
    # Ajustar diseño
    fig.update_traces(
        textposition='inside',
        textinfo='percent',
        insidetextorientation='radial',
        hoverinfo='label+percent',
        marker=dict(line=dict(color='white', width=2))
    )
    
    fig.update_layout(
        height=300,
        margin=dict(l=20, r=20, t=40, b=20),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.2,
            xanchor="center",
            x=0.5
        )
    )
    
    # Mostrar el gráfico
    st.plotly_chart(fig, use_container_width=True)

def mostrar_pagina_demografia():
    """
    Muestra el contenido de la pestaña DEMOGRAFÍA con visualizaciones
    de consumo de proteínas y otros alimentos.
    """
    st.header("Perfil de Consumo Alimentario")
    
    # Verificar si hay datos cargados en la sesión
    if 'df' in st.session_state:
        df = st.session_state.df
        st.success(f"Usando datos cargados. Total de filas: {len(df)}")
    else:
        # Si no hay datos cargados, intentar cargarlos
        from google_connection import load_data
        with st.spinner("Cargando datos desde Google Sheets..."):
            try:
                # Cargar los datos desde la hoja "DUB"
                sheet_id = "1haZINioOFe4WTL2G9FzsYt0p4-8uJ5WKbukexBYhx_o"
                df = load_data(sheet_id, "DUB")
                
                if df is not None and not df.empty:
                    # Guardar en session_state para compartirlo entre pestañas
                    st.session_state.df = df
                    st.success(f"Datos cargados correctamente. Total de filas: {len(df)}")
                else:
                    st.error("No se pudieron cargar los datos.")
                    return
            except Exception as e:
                st.error(f"Error en la aplicación: {e}")
                return
    
    # Posiciones de las columnas en el dataframe (basado en los índices proporcionados)
    # BS = 70, BT = 71, BU = 72, BV = 73, BW = 74, BX = 75 (0-indexado)
    posiciones = {
        'carnes_rojas': 70,           # BS
        'Pollo': 71,                  # BT
        'Pescado': 72,                # BU
        'Huevo': 73,                  # BV
        'Consumo_frutas_verduras': 74, # BW
        'Consumo_lácteos': 75         # BX
    }
    
    # Diccionario de imágenes asociadas a cada columna
    imagenes = {
        'carnes_rojas': 'bife',
        'Pollo': 'pollo',
        'Pescado': 'pez',
        'Huevo': 'huevos',
        'Consumo_frutas_verduras': 'comida-sana',
        'Consumo_lácteos': 'productos-lacteos'
    }
    
    # Títulos para los gráficos
    titulos = {
        'carnes_rojas': 'Consumo de Carnes Rojas',
        'Pollo': 'Consumo de Pollo',
        'Pescado': 'Consumo de Pescado',
        'Huevo': 'Consumo de Huevo',
        'Consumo_frutas_verduras': 'Consumo de Frutas y Verduras',
        'Consumo_lácteos': 'Consumo de Lácteos'
    }
    
    # Crear dos filas, cada una con tres columnas
    st.subheader("Consumo de Proteínas y Alimentos")
    
    # Primera fila
    st.markdown("### Consumo de Proteínas")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        crear_grafico_pastel_con_imagen(
            df, 
            'carnes_rojas', 
            titulos['carnes_rojas'], 
            imagenes['carnes_rojas'], 
            posiciones['carnes_rojas']
        )
    
    with col2:
        crear_grafico_pastel_con_imagen(
            df, 
            'Pollo', 
            titulos['Pollo'], 
            imagenes['Pollo'], 
            posiciones['Pollo']
        )
    
    with col3:
        crear_grafico_pastel_con_imagen(
            df, 
            'Pescado', 
            titulos['Pescado'], 
            imagenes['Pescado'], 
            posiciones['Pescado']
        )
    
    # Segunda fila
    st.markdown("### Consumo de Otros Alimentos")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        crear_grafico_pastel_con_imagen(
            df, 
            'Huevo', 
            titulos['Huevo'], 
            imagenes['Huevo'], 
            posiciones['Huevo']
        )
    
    with col2:
        crear_grafico_pastel_con_imagen(
            df, 
            'Consumo_frutas_verduras', 
            titulos['Consumo_frutas_verduras'], 
            imagenes['Consumo_frutas_verduras'], 
            posiciones['Consumo_frutas_verduras']
        )
    
    with col3:
        crear_grafico_pastel_con_imagen(
            df, 
            'Consumo_lácteos', 
            titulos['Consumo_lácteos'], 
            imagenes['Consumo_lácteos'], 
            posiciones['Consumo_lácteos']
        )
    
    # Agregar información adicional
    st.markdown("---")
    st.markdown("""
    ### Interpretación de los datos
    
    Esta visualización muestra la distribución de la frecuencia de consumo de diferentes grupos de alimentos 
    entre los beneficiarios registrados en el sistema DUB. Los gráficos permiten identificar patrones 
    de consumo alimentario que pueden ser útiles para la planificación de programas nutricionales.
    """)

if __name__ == "__main__":
    st.set_page_config(layout="wide")
    mostrar_pagina_demografia()