import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import json
import uuid
from streamlit.components.v1 import html

def plotly_events(fig, click_event=True, select_event=False, hover_event=False, override_height=None):
    """
    Función para capturar eventos de Plotly.
    
    Parámetros:
    - fig: figura de Plotly
    - click_event: capturar eventos de clic
    - select_event: capturar eventos de selección
    - hover_event: capturar eventos de hover
    - override_height: altura personalizada
    
    Retorna:
    - Lista de puntos seleccionados
    """
    # Generar un ID único para este componente
    div_id = f"plotly-{uuid.uuid4()}"
    
    # Configurar qué eventos capturar
    event_names = []
    if click_event:
        event_names.append("click")
    if select_event:
        event_names.append("select")
    if hover_event:
        event_names.append("hover")
    
    # Variable para almacenar los puntos seleccionados
    selected_points_key = f"{div_id}-selected-points"
    if selected_points_key not in st.session_state:
        st.session_state[selected_points_key] = []
    
    # Convertir la figura a JSON
    fig_json = fig.to_json()
    
    # Crear el HTML personalizado con el gráfico y los manejadores de eventos
    component_html = f"""
    <div id="{div_id}"></div>
    <script>
        // Asegurarse de que Plotly esté disponible
        if (window.Plotly) {{
            var fig = {fig_json};
            Plotly.newPlot("{div_id}", fig.data, fig.layout, {{responsive: true}});
            
            var selected_points = [];
            
            // Manejar eventos
            {div_id}.on("plotly_click", function(data) {{
                selected_points = [];
                var point = data.points[0];
                selected_points.push({{
                    curveNumber: point.curveNumber,
                    pointNumber: point.pointNumber,
                    pointIndex: point.pointIndex,
                    x: point.x,
                    y: point.y
                }});
                console.log("Punto seleccionado:", selected_points);
                
                // Enviar los datos al backend de Streamlit
                const json_data = JSON.stringify(selected_points);
                window.parent.postMessage({{
                    type: "streamlit:setComponentValue",
                    value: json_data
                }}, "*");
            }});
        }}
    </script>
    """
    
    # Crear componente HTML
    selected_points_json = html(
        component_html,
        height=override_height if override_height else fig.layout.height or 400,
        key=div_id
    )
    
    # Procesar respuesta
    if selected_points_json:
        try:
            selected_points = json.loads(selected_points_json)
            st.session_state[selected_points_key] = selected_points
            return selected_points
        except:
            return []
    
    return st.session_state[selected_points_key]

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
    Muestra múltiples filas de gráficos de barras horizontales organizados por temática
    """
    st.markdown("### Distribuciones Demográficas")
    
    # Mapa de posiciones (columna, índice)
    posiciones = {
        'Estado_civil': 36,               # AK
        'Nivel_escolaridad': 40,          # AO
        'Estado_escolaridad': 41,         # AP
        'Ocupacion_actual': 42,           # AQ
        'Seguridad_social': 43,           # AR
        'Cuántas_horas_al_día_dedica_a_hacer_los_oficios_del_hogar': 44, # AS
        'Tipo_de_discapacidad': 45,       # AT
        'Registro_Único_de_Víctimas_RUV': 47, # AV
        'Se_considera_campesino': 48,     # AW
        'Se_reconoce_como': 37,           # AL
        'A_que_pueblo': 39                # AN
    }
    
    # Verificar y asignar columnas por posición si es necesario
    columnas = list(df.columns)
    for nombre_col, indice in posiciones.items():
        if nombre_col not in df.columns and len(columnas) > indice:
            df[nombre_col] = df[columnas[indice]]
    
    # PRIMERA FILA: Nivel y Estado de Escolaridad
    st.markdown("#### Educación")
    
    # Inicializar estado de sesión para el filtro seleccionado
    if 'nivel_educativo_seleccionado' not in st.session_state:
        st.session_state.nivel_educativo_seleccionado = None
    
    # Crear columnas con distribución 60/40
    col1, col2 = st.columns([6, 4])
    
    with col1:
        # Crear gráfico interactivo de barras con selección
        if 'Nivel_escolaridad' in df.columns:
            conteo = df['Nivel_escolaridad'].value_counts()
            data_plot = pd.DataFrame({
                'Categoría': conteo.index,
                'Cantidad': conteo.values
            })
            
            # Ordenar para mejor visualización
            data_plot = data_plot.sort_values('Cantidad', ascending=True)
            
            # Calcular porcentajes
            total = conteo.sum()
            data_plot['Porcentaje'] = (data_plot['Cantidad'] / total * 100).round(1)
            
            # Crear gráfico de barras con Plotly
            fig = px.bar(
                data_plot,
                y='Categoría',
                x='Cantidad',
                title="Nivel de Escolaridad (Selecciona para filtrar)",
                color='Cantidad',
                color_continuous_scale="Blues",
                text=data_plot['Porcentaje'].apply(lambda x: f"{x:.1f}%")
            )
            
            # Configurar diseño
            fig.update_traces(
                textposition='auto',
                hovertemplate='<b>%{y}</b><br>Cantidad: %{x}<br>Porcentaje: %{text}<extra></extra>',
                marker_line_color='white',
                marker_line_width=0.5,
                opacity=0.8
            )
            
            fig.update_layout(
                height=400,
                margin=dict(l=20, r=20, t=50, b=20),
                xaxis_title="Cantidad",
                yaxis_title="",
                coloraxis_showscale=False
            )
            
            # Mostrar gráfico con Streamlit
            st.plotly_chart(fig, use_container_width=True)
            
            # Crear selector para filtrar
            nivel_options = ["Todos"] + sorted(conteo.index.tolist())
            selected_level = st.selectbox(
                "Filtrar por nivel educativo:",
                nivel_options,
                index=0
            )
            
            # Actualizar el filtro basado en la selección
            if selected_level != "Todos":
                st.session_state.nivel_educativo_seleccionado = selected_level
            else:
                st.session_state.nivel_educativo_seleccionado = None
            
        else:
            st.warning("No se encontró la columna 'Nivel_escolaridad' en los datos")
    
    with col2:
        # Crear gráfico de pastel para estado de escolaridad con filtro aplicado
        if 'Estado_escolaridad' in df.columns:
            # Aplicar filtro si existe
            df_filtrado = df
            titulo = "Estado de Escolaridad"
            
            if st.session_state.nivel_educativo_seleccionado:
                df_filtrado = df[df['Nivel_escolaridad'] == st.session_state.nivel_educativo_seleccionado]
                titulo = f"Estado para {st.session_state.nivel_educativo_seleccionado}"
            
            # Crear gráfico de pastel
            fig_pastel = crear_grafico_pastel(df_filtrado, 'Estado_escolaridad', titulo)
            if fig_pastel:
                st.plotly_chart(fig_pastel, use_container_width=True)
                
                # Información sobre el filtro
                if st.session_state.nivel_educativo_seleccionado:
                    total_filtrado = len(df_filtrado)
                    porcentaje = (total_filtrado / len(df) * 100)
                    st.markdown(f"Mostrando **{total_filtrado:,}** registros ({porcentaje:.2f}% del total)")
            else:
                st.warning("No hay datos suficientes para mostrar este gráfico")
        else:
            st.warning("No se encontró la columna 'Estado_escolaridad' en los datos")
    
    # SEGUNDA FILA: Estado Civil y Ocupación Actual
    st.markdown("#### Situación Personal y Laboral")
    col1, col2 = st.columns(2)
    
    with col1:
        fig = crear_grafico_barras_horizontal(df, 'Estado_civil', "Estado Civil")
        if fig:
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = crear_grafico_barras_horizontal(df, 'Ocupacion_actual', "Ocupación Actual")
        if fig:
            st.plotly_chart(fig, use_container_width=True)
    
    # TERCERA FILA: Registro de Víctimas y Se Considera Campesino (anteriormente era Condiciones de Salud)
    st.markdown("#### Condiciones Sociales")
    col1, col2 = st.columns(2)
    
    with col1:
        fig = crear_grafico_barras_horizontal(df, 'Registro_Único_de_Víctimas_RUV', "Registro Único de Víctimas")
        if fig:
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = crear_grafico_barras_horizontal(df, 'Se_considera_campesino', "Se Considera Campesino")
        if fig:
            st.plotly_chart(fig, use_container_width=True)
    
    # CUARTA FILA: Horas de oficios del hogar y Se reconoce como
    st.markdown("#### Condiciones del Hogar y Reconocimiento")
    col1, col2 = st.columns(2)
    
    with col1:
        fig = crear_grafico_barras_horizontal(
            df, 
            'Cuántas_horas_al_día_dedica_a_hacer_los_oficios_del_hogar', 
            "Horas Diarias en Oficios del Hogar"
        )
        if fig:
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = crear_grafico_barras_horizontal(df, 'Se_reconoce_como', "Se Reconoce Como")
        if fig:
            st.plotly_chart(fig, use_container_width=True)
    
    # QUINTA FILA: Seguridad Social y Tipo de Discapacidad (Tablas)
    st.markdown("#### Condiciones de Salud")
    
    # Inicializar estado de sesión para el filtro de seguridad social
    if 'seguridad_social_seleccionada' not in st.session_state:
        st.session_state.seguridad_social_seleccionada = None
    
    # Crear dos columnas
    col1, col2 = st.columns(2)
    
    with col1:
        # Tabla para Seguridad Social
        if 'Seguridad_social' in df.columns:
            st.subheader("Seguridad Social")
            
            # Crear tabla de frecuencias
            conteo_seguridad = df['Seguridad_social'].value_counts().reset_index()
            conteo_seguridad.columns = ['Tipo de Seguridad Social', 'Cantidad']
            
            # Calcular porcentajes
            total = conteo_seguridad['Cantidad'].sum()
            conteo_seguridad['Porcentaje'] = (conteo_seguridad['Cantidad'] / total * 100).round(2).astype(str) + '%'
            
            # Formatear números con separador de miles
            conteo_seguridad['Cantidad'] = conteo_seguridad['Cantidad'].apply(lambda x: f"{x:,}")
            
            # Mostrar tabla
            st.dataframe(conteo_seguridad, use_container_width=True, height=400)
            
            # Crear selector para filtrar
            valores_seguridad = ["Todos"] + sorted(df['Seguridad_social'].dropna().unique().tolist())
            selected_seguridad = st.selectbox(
                "Filtrar tabla de discapacidad por tipo de seguridad social:",
                valores_seguridad,
                index=0,
                key="selector_seguridad_social"
            )
            
            # Actualizar el filtro basado en la selección
            if selected_seguridad != "Todos":
                st.session_state.seguridad_social_seleccionada = selected_seguridad
            else:
                st.session_state.seguridad_social_seleccionada = None
        else:
            st.warning("No se encontró la columna 'Seguridad_social' en los datos")
    
    with col2:
        # Tabla para Tipo de Discapacidad con filtro aplicado
        if 'Tipo_de_discapacidad' in df.columns:
            # Aplicar filtro si existe
            df_filtrado = df
            titulo = "Tipo de Discapacidad"
            
            if st.session_state.seguridad_social_seleccionada:
                df_filtrado = df[df['Seguridad_social'] == st.session_state.seguridad_social_seleccionada]
                titulo = f"Discapacidad con {st.session_state.seguridad_social_seleccionada}"
            
            st.subheader(titulo)
            
            # Crear tabla de frecuencias
            conteo_discapacidad = df_filtrado['Tipo_de_discapacidad'].value_counts().reset_index()
            conteo_discapacidad.columns = ['Tipo de Discapacidad', 'Cantidad']
            
            # Calcular porcentajes
            total_disc = conteo_discapacidad['Cantidad'].sum()
            conteo_discapacidad['Porcentaje'] = (conteo_discapacidad['Cantidad'] / total_disc * 100).round(2).astype(str) + '%'
            
            # Formatear números con separador de miles
            conteo_discapacidad['Cantidad'] = conteo_discapacidad['Cantidad'].apply(lambda x: f"{x:,}")
            
            # Mostrar tabla
            st.dataframe(conteo_discapacidad, use_container_width=True, height=400)
            
            # Información sobre el filtro
            if st.session_state.seguridad_social_seleccionada:
                total_filtrado = len(df_filtrado)
                porcentaje = (total_filtrado / len(df) * 100)
                st.markdown(f"Mostrando **{total_filtrado:,}** registros ({porcentaje:.2f}% del total)")
        else:
            st.warning("No se encontró la columna 'Tipo_de_discapacidad' en los datos")