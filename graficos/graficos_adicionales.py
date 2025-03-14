import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

def crear_grafico_pastel(df, columna, titulo=None, limite_categorias=10):
    """
    Crea un gráfico de pastel para la columna especificada.
    
    Args:
        df: DataFrame con los datos
        columna: Nombre de la columna a graficar
        titulo: Título del gráfico (opcional)
        limite_categorias: Número máximo de categorías a mostrar
    
    Returns:
        fig: Figura de Plotly con el gráfico
    """
    if columna not in df.columns:
        st.warning(f"No se encontró la columna '{columna}' en los datos")
        return None
    
    # Obtener el conteo de valores
    conteo = df[columna].value_counts()
    
    # Si hay más categorías que el límite, agrupar las menos frecuentes como "Otros"
    if len(conteo) > limite_categorias:
        principales = conteo.nlargest(limite_categorias - 1)
        otros = pd.Series({'Otros': conteo[~conteo.index.isin(principales.index)].sum()})
        conteo = pd.concat([principales, otros])
    
    # Calcular porcentajes
    total = conteo.sum()
    porcentajes = (conteo / total * 100).round(1)
    
    # Crear etiquetas con porcentajes
    etiquetas = [f"{idx} ({val:.1f}%)" for idx, val in zip(conteo.index, porcentajes)]
    
    # Crear gráfico
    fig = px.pie(
        values=conteo.values,
        names=etiquetas,
        title=titulo if titulo else f"Distribución por {columna}",
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
        height=400,
        margin=dict(l=20, r=20, t=40, b=20),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.2,
            xanchor="center",
            x=0.5
        )
    )
    
    return fig

def crear_grafico_barras_horizontal(df, columna, titulo=None, limite_categorias=15, color="Blues"):
    """
    Crea un gráfico de barras horizontales para la columna especificada.
    
    Args:
        df: DataFrame con los datos
        columna: Nombre de la columna a graficar
        titulo: Título del gráfico (opcional)
        limite_categorias: Número máximo de categorías a mostrar
        color: Escala de color para el gráfico
    
    Returns:
        fig: Figura de Plotly con el gráfico
    """
    if columna not in df.columns:
        st.warning(f"No se encontró la columna '{columna}' en los datos")
        return None
    
    # Obtener el conteo de valores y ordenar de mayor a menor
    conteo = df[columna].value_counts().nlargest(limite_categorias)
    
    # Crear dataframe para plotly
    data_plot = pd.DataFrame({
        'Categoría': conteo.index,
        'Cantidad': conteo.values
    })
    
    # Calcular porcentajes
    total = conteo.sum()
    data_plot['Porcentaje'] = (data_plot['Cantidad'] / total * 100).round(1)
    
    # Ordenar de mayor a menor
    data_plot = data_plot.sort_values('Cantidad', ascending=True)
    
    # Crear gráfico
    fig = px.bar(
        data_plot,
        y='Categoría',
        x='Cantidad',
        title=titulo if titulo else f"Distribución por {columna}",
        color='Cantidad',
        color_continuous_scale=color,
        text=data_plot['Porcentaje'].apply(lambda x: f"{x:.1f}%")
    )
    
    # Ajustar diseño
    fig.update_traces(
        textposition='auto',
        hovertemplate='<b>%{y}</b><br>Cantidad: %{x}<br>Porcentaje: %{text}<extra></extra>'
    )
    
    fig.update_layout(
        height=300,  # Altura ajustada para que quepan en la matriz
        margin=dict(l=20, r=20, t=40, b=20),
        xaxis_title="Cantidad",
        yaxis_title="",
        coloraxis_showscale=False
    )
    
    return fig

def mostrar_graficos_pastel(df):
    """
    Muestra los gráficos de pastel para identidad y orientación sexual
    """
    st.markdown("### Distribución por Identidad y Orientación Sexual")
    
    # Crear dos columnas
    col1, col2 = st.columns(2)
    
    # Columna 1: Identidad
    with col1:
        # Buscar la columna por nombre o posición
        columna_identidad = 'Uste_se_identifica_como'
        if columna_identidad not in df.columns:
            # Intentar por posición (AI sería la columna 34, 0-indexado)
            columnas = list(df.columns)
            if len(columnas) >= 35:
                columna_ai = columnas[34]
                df[columna_identidad] = df[columna_ai]
        
        # Crear gráfico de identidad
        fig_identidad = crear_grafico_pastel(
            df, 
            columna_identidad, 
            titulo="¿Usted se identifica como?"
        )
        if fig_identidad:
            st.plotly_chart(fig_identidad, use_container_width=True)
    
    # Columna 2: Orientación Sexual
    with col2:
        # Buscar la columna por nombre o posición
        columna_orientacion = 'Orientación_sexual'
        if columna_orientacion not in df.columns:
            # Intentar por posición (AJ sería la columna 35, 0-indexado)
            columnas = list(df.columns)
            if len(columnas) >= 36:
                columna_aj = columnas[35]
                df[columna_orientacion] = df[columna_aj]
        
        # Crear gráfico de orientación sexual
        fig_orientacion = crear_grafico_pastel(
            df, 
            columna_orientacion, 
            titulo="Orientación Sexual"
        )
        if fig_orientacion:
            st.plotly_chart(fig_orientacion, use_container_width=True)

def mostrar_matriz_graficos_barras(df):
    """
    Muestra una matriz 3x4 de gráficos de barras horizontales
    """
    st.markdown("### Matriz de Distribuciones Demográficas")
    
    # Definir las columnas a mostrar
    columnas_matriz = [
        'Estado_civil',            # AK (36)
        'Nivel_escolaridad',       # AO (40)
        'Estado_escolaridad',      # AP (41)
        'Ocupacion_actual',        # AQ (42)
        'Seguridad_social',        # AR (43)
        'Cuántas_horas_al_día_dedica_a_hacer_los_oficios_del_hogar', # AS (44)
        'Tipo_de_discapacidad',    # AT (45)
        'Registro_Único_de_Víctimas_RUV', # AV (47)
        'Se_considera_campesino',   # AW (48)
        # Relleno con dos columnas vacías para completar la matriz 3x4
        None,
        None
    ]
    
    # Mapa de posiciones (columna, índice)
    posiciones = {
        'Estado_civil': 36,
        'Nivel_escolaridad': 40,
        'Estado_escolaridad': 41,
        'Ocupacion_actual': 42,
        'Seguridad_social': 43,
        'Cuántas_horas_al_día_dedica_a_hacer_los_oficios_del_hogar': 44,
        'Tipo_de_discapacidad': 45,
        'Registro_Único_de_Víctimas_RUV': 47,
        'Se_considera_campesino': 48
    }
    
    # Verificar y asignar columnas por posición si es necesario
    columnas = list(df.columns)
    for nombre_col, indice in posiciones.items():
        if nombre_col not in df.columns and len(columnas) > indice:
            df[nombre_col] = df[columnas[indice]]
    
    # Crear una matriz 3x4 (3 filas, 4 columnas)
    for i in range(0, len(columnas_matriz), 4):
        # Crear fila de 4 columnas
        cols = st.columns(4)
        
        # Añadir hasta 4 gráficos en esta fila
        for j in range(4):
            idx = i + j
            if idx < len(columnas_matriz) and columnas_matriz[idx] is not None:
                with cols[j]:
                    columna = columnas_matriz[idx]
                    titulo = columna.replace('_', ' ').title()
                    fig = crear_grafico_barras_horizontal(df, columna, titulo)
                    if fig:
                        st.plotly_chart(fig, use_container_width=True)