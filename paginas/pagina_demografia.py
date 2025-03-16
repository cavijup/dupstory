import streamlit as st
import pandas as pd
import plotly.express as px
import os

def crear_grafico_pastel_con_imagen(df, columna, titulo, imagen_nombre, posicion_columna=None, mostrar_leyenda=False):
    """
    Crea un gráfico de pastel con una imagen relacionada arriba.
    
    Args:
        df: DataFrame con los datos
        columna: Nombre de la columna a mostrar
        titulo: Título a mostrar para el gráfico
        imagen_nombre: Nombre del archivo de imagen (sin extensión)
        posicion_columna: Índice de la columna si no se encuentra por nombre
        mostrar_leyenda: Si es True, muestra la leyenda del gráfico
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
    etiquetas = [f"{idx}" for idx in conteo.index]
    
    # Crear gráfico de pastel con Plotly
    fig = px.pie(
        values=conteo.values,
        names=etiquetas,
        title=None,
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
        showlegend=mostrar_leyenda
    )
    
    # Si es gráfico con leyenda, ajustar posición de la leyenda
    if mostrar_leyenda:
        fig.update_layout(
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
    
    return conteo

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
    
    # Obtener todas las categorías únicas de respuestas para la convención
    all_categories = set()
    for col_name, col_pos in posiciones.items():
        if col_name in df.columns:
            all_categories.update(df[col_name].dropna().unique())
        elif len(df.columns) > col_pos:
            all_categories.update(df.iloc[:, col_pos].dropna().unique())
    
    # Crear una tabla explicativa para la convención
    st.markdown("### Convenciones")
    st.write("Las siguientes categorías aparecen en los gráficos de consumo alimentario:")
    
    # Crear un dataframe con las categorías y sus descripciones
    category_descriptions = {
        "DIARIO": "Consumo todos los días",
        "SEMANAL": "Consumo algunas veces por semana",
        "QUINCENAL": "Consumo aproximadamente cada 15 días",
        "MENSUAL": "Consumo aproximadamente una vez al mes",
        "OCASIONAL": "Consumo rara vez o en ocasiones especiales",
        "NO CONSUME": "No consume este tipo de alimento"
    }
    
    # Mostrar las descripciones en forma de tabla
    categorias_data = []
    for cat in sorted(all_categories):
        if pd.notna(cat) and cat.strip():
            desc = category_descriptions.get(cat, "Sin descripción disponible")
            categorias_data.append({"Categoría": cat, "Descripción": desc})
    
    if categorias_data:
        st.table(pd.DataFrame(categorias_data))
    
    # Primera fila
    st.markdown("### Consumo de Proteínas")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        crear_grafico_pastel_con_imagen(
            df, 
            'carnes_rojas', 
            titulos['carnes_rojas'], 
            imagenes['carnes_rojas'], 
            posiciones['carnes_rojas'],
            mostrar_leyenda=False
        )
    
    with col2:
        crear_grafico_pastel_con_imagen(
            df, 
            'Pollo', 
            titulos['Pollo'], 
            imagenes['Pollo'], 
            posiciones['Pollo'],
            mostrar_leyenda=False
        )
    
    with col3:
        crear_grafico_pastel_con_imagen(
            df, 
            'Pescado', 
            titulos['Pescado'], 
            imagenes['Pescado'], 
            posiciones['Pescado'],
            mostrar_leyenda=False
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
            posiciones['Huevo'],
            mostrar_leyenda=False
        )
    
    with col2:
        crear_grafico_pastel_con_imagen(
            df, 
            'Consumo_frutas_verduras', 
            titulos['Consumo_frutas_verduras'], 
            imagenes['Consumo_frutas_verduras'], 
            posiciones['Consumo_frutas_verduras'],
            mostrar_leyenda=False
        )
    
    with col3:
        crear_grafico_pastel_con_imagen(
            df, 
            'Consumo_lácteos', 
            titulos['Consumo_lácteos'], 
            imagenes['Consumo_lácteos'], 
            posiciones['Consumo_lácteos'],
            mostrar_leyenda=False
        )
    
    # Agregar información adicional
    st.markdown("---")
    
    # Crear resumen estadístico
    st.markdown("### Resumen Estadístico")
    
    # Crear un mapa de colores para las categorías
    color_map = {
        "DIARIO": "#1f77b4",    # Azul oscuro
        "SEMANAL": "#2ca02c",   # Verde
        "QUINCENAL": "#ff7f0e", # Naranja
        "MENSUAL": "#d62728",   # Rojo
        "OCASIONAL": "#9467bd", # Púrpura
        "NO CONSUME": "#7f7f7f" # Gris
    }
    
    # Preparar datos para el resumen
    consumo_data = {}
    for col_name, col_pos in posiciones.items():
        conteo = None
        if col_name in df.columns:
            conteo = df[col_name].value_counts()
        elif len(df.columns) > col_pos:
            columnas = list(df.columns)
            conteo = df[columnas[col_pos]].value_counts()
            
        if conteo is not None:
            consumo_data[titulos[col_name]] = conteo
    
    # Crear dos columnas para la visualización
    col1, col2 = st.columns([3, 2])
    
    with col1:
        # Crear gráfico de resumen
        if consumo_data:
            st.markdown("#### Comparativa de patrones de consumo")
            
            # Convertir los datos a un formato adecuado para visualización
            summary_data = []
            for alimento, conteo in consumo_data.items():
                total = conteo.sum()
                for categoria, valor in conteo.items():
                    if pd.notna(categoria) and categoria.strip():
                        porcentaje = (valor / total * 100).round(1)
                        summary_data.append({
                            "Alimento": alimento,
                            "Categoría": categoria,
                            "Porcentaje": porcentaje
                        })
            
            if summary_data:
                summary_df = pd.DataFrame(summary_data)
                
                # Crear gráfico de barras agrupadas
                fig = px.bar(
                    summary_df,
                    x="Alimento",
                    y="Porcentaje",
                    color="Categoría",
                    barmode="group",
                    color_discrete_map=color_map,
                    title="Comparativa de frecuencia de consumo por tipo de alimento"
                )
                
                fig.update_layout(
                    xaxis_title="Tipo de Alimento",
                    yaxis_title="Porcentaje (%)",
                    legend_title="Frecuencia de Consumo",
                    height=400
                )
                
                st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("#### Conclusiones")
        st.markdown("""
        Esta visualización muestra la distribución de la frecuencia de consumo de diferentes grupos de alimentos 
        entre los beneficiarios registrados en el sistema DUB. Los gráficos permiten identificar patrones 
        de consumo alimentario que pueden ser útiles para la planificación de programas nutricionales.
        
        Aspectos a considerar:
        
        - La frecuencia de consumo de proteínas animales
        - El consumo regular de frutas y verduras
        - La ingesta de lácteos y su relación con la nutrición
        
        Estos datos pueden usarse para orientar acciones específicas en los comedores comunitarios y programas 
        de seguridad alimentaria.
        """)

if __name__ == "__main__":
    st.set_page_config(layout="wide")
    mostrar_pagina_demografia()