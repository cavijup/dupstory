import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

def crear_grafico_pastel_con_imagen(df, columna, titulo, imagen_nombre, posicion_columna=None, mostrar_leyenda=False, color_map=None):
    """
    Crea un gráfico de pastel con una imagen relacionada arriba.
    
    Args:
        df: DataFrame con los datos
        columna: Nombre de la columna a mostrar
        titulo: Título a mostrar para el gráfico
        imagen_nombre: Nombre del archivo de imagen (sin extensión)
        posicion_columna: Índice de la columna si no se encuentra por nombre
        mostrar_leyenda: Si es True, muestra la leyenda del gráfico
        color_map: Diccionario que mapea categorías a colores
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
    
    # Crear etiquetas
    etiquetas = conteo.index.tolist()
    
    # Preparar datos para el gráfico
    pie_data = pd.DataFrame({
        'categoria': etiquetas,
        'valor': conteo.values
    })
    
    # Asignar colores basados en el mapa de colores si se proporciona
    colores = None
    if color_map:
        colores = [color_map.get(cat, "#808080") for cat in etiquetas]
    
    # Crear gráfico de pastel con Plotly
    fig = px.pie(
        pie_data,
        values='valor',
        names='categoria',
        title=None,
        color='categoria',
        color_discrete_map={cat: color for cat, color in zip(etiquetas, colores)} if colores else None,
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
    
    # Mapa de colores para las categorías de frecuencia
    color_map = {
        "DE 2 A 3 VECES A LA SEMANA": "#8BC34A",  # Verde claro
        "NO CONSUMI ESTE ALIMENTO": "#F44336",    # Rojo
        "NO CONSUMÍ FRUTAS NI VERDURAS": "#FFEB3B", # Amarillo
        "NO SABE NO RESPONDE": "#9E9E9E",         # Gris
        "TODOS LOS DÍAS": "#2E7D32",              # Verde oscuro
        "1 VEZ A LA SEMANA": "#ffb700",           # Naranja
        "DIARIO": "#2E7D32",                      # Verde oscuro (alternativo)
        "SEMANAL": "#8BC34A",                     # Verde claro (alternativo)
        "QUINCENAL": "#CDDC39",                   # Lima
        "MENSUAL": "#03A9F4",                     # Azul claro
        "OCASIONAL": "#9C27B0",                   # Púrpura
        "NO CONSUME": "#F44336"                   # Rojo (alternativo)
    }
    # Obtener todas las categorías únicas de respuestas
    all_categories = set()
    for col_name, col_pos in posiciones.items():
        if col_name in df.columns:
            all_categories.update(df[col_name].dropna().unique())
        elif len(df.columns) > col_pos:
            # Corregir para obtener las categorías del DataFrame usando posición
            columnas = list(df.columns)
            all_categories.update(df[columnas[col_pos]].dropna().unique())
    
    # Filtrar categorías vacías o nulas
    all_categories = [cat for cat in all_categories if pd.notna(cat) and str(cat).strip()]
    
    # REEMPLAZO DEL SISTEMA DE FILTROS CON LEYENDA DE COLORES
    st.markdown("### Leyenda de Colores para la Frecuencia de Consumo")
    
    # Crea columnas para mostrar las leyendas de colores
    cols = st.columns(3)
    i = 0
    
    # Muestra cada categoría con su color correspondiente
    for categoria in sorted(all_categories):
        with cols[i % 3]:
            color = color_map.get(categoria, "#808080")
            st.markdown(
                f"""
                <div style="
                    background-color: {color};
                    width: 20px;
                    height: 20px;
                    display: inline-block;
                    margin-right: 10px;
                    border-radius: 3px;
                "></div>
                <span style="vertical-align: middle">{categoria}</span>
                """,
                unsafe_allow_html=True
            )
        i += 1
    
    # En la variable selected_categories, todas las categorías están seleccionadas
    selected_categories = {cat: True for cat in all_categories}
    st.session_state.selected_categories = selected_categories
    
    # Primera fila de gráficos
    st.markdown("### Consumo de Proteínas")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        crear_grafico_pastel_con_imagen(
            df, 
            'carnes_rojas', 
            titulos['carnes_rojas'], 
            imagenes['carnes_rojas'], 
            posiciones['carnes_rojas'],
            mostrar_leyenda=False,
            color_map=color_map
        )
    
    with col2:
        crear_grafico_pastel_con_imagen(
            df, 
            'Pollo', 
            titulos['Pollo'], 
            imagenes['Pollo'], 
            posiciones['Pollo'],
            mostrar_leyenda=False,
            color_map=color_map
        )
    
    with col3:
        crear_grafico_pastel_con_imagen(
            df, 
            'Pescado', 
            titulos['Pescado'], 
            imagenes['Pescado'], 
            posiciones['Pescado'],
            mostrar_leyenda=False,
            color_map=color_map
        )
    
    # Segunda fila de gráficos
    st.markdown("### Consumo de Otros Alimentos")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        crear_grafico_pastel_con_imagen(
            df, 
            'Huevo', 
            titulos['Huevo'], 
            imagenes['Huevo'], 
            posiciones['Huevo'],
            mostrar_leyenda=False,
            color_map=color_map
        )
    
    with col2:
        crear_grafico_pastel_con_imagen(
            df, 
            'Consumo_frutas_verduras', 
            titulos['Consumo_frutas_verduras'], 
            imagenes['Consumo_frutas_verduras'], 
            posiciones['Consumo_frutas_verduras'],
            mostrar_leyenda=False,
            color_map=color_map
        )
    
    with col3:
        crear_grafico_pastel_con_imagen(
            df, 
            'Consumo_lácteos', 
            titulos['Consumo_lácteos'], 
            imagenes['Consumo_lácteos'], 
            posiciones['Consumo_lácteos'],
            mostrar_leyenda=False,
            color_map=color_map
        )
        # Agregar información adicional
    st.markdown("---")
    
    # Crear resumen estadístico
    st.markdown("### Resumen Estadístico")
    
    # Preparar datos para el resumen, considerando solamente las categorías seleccionadas
    consumo_data = {}
    for col_name, col_pos in posiciones.items():
        conteo = None
        if col_name in df.columns:
            # Aplicar filtro a una copia de la serie para evitar advertencias
            serie = df[col_name].copy()
            filtro = serie.isin([cat for cat, selected in selected_categories.items() if selected])
            conteo = serie[filtro].value_counts()
        elif len(df.columns) > col_pos:
            columnas = list(df.columns)
            serie = df[columnas[col_pos]].copy()
            filtro = serie.isin([cat for cat, selected in selected_categories.items() if selected])
            conteo = serie[filtro].value_counts()
            
        if conteo is not None and not conteo.empty:
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
                    if pd.notna(categoria) and categoria.strip() and selected_categories.get(categoria, False):
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
                    height=450,
                    margin=dict(l=20, r=20, t=50, b=100)
                )
                
                # Rotar etiquetas del eje x para mejor legibilidad
                fig.update_xaxes(tickangle=45)
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Agregar tabla de resumen con los porcentajes
                st.markdown("#### Tabla de resumen")
                
                # Crear una tabla pivote con los alimentos como filas y categorías como columnas
                try:
                    pivot_table = summary_df.pivot_table(
                        index='Alimento', 
                        columns='Categoría', 
                        values='Porcentaje', 
                        aggfunc='sum'
                    ).fillna(0).round(1)
                    
                    # Agregar una columna de total
                    pivot_table['TOTAL'] = pivot_table.sum(axis=1)
                    
                    # Formatear la tabla para mostrar
                    pivot_display = pivot_table.copy()
                    for col in pivot_display.columns:
                        pivot_display[col] = pivot_display[col].apply(lambda x: f"{x}%")
                    
                    st.dataframe(pivot_display, use_container_width=True)
                except Exception as e:
                    st.warning(f"No se pudo generar la tabla de resumen: {e}")
            else:
                st.warning("No hay datos suficientes para generar el gráfico comparativo. Por favor, selecciona al menos una categoría.")
        else:
            st.warning("No hay datos para generar el resumen estadístico con los filtros actuales.")
    
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
            
        # Añadir métricas de resumen
        st.markdown("#### Métricas Destacadas")
        
        try:
            # Calcular algunas métricas importantes
            metricas = []
            for col_name, col_pos in posiciones.items():
                if col_name in df.columns:
                    serie = df[col_name]
                elif len(df.columns) > col_pos:
                    columnas = list(df.columns)
                    serie = df[columnas[col_pos]]
                else:
                    continue
                    
                # Calcular porcentaje de consumo diario (usando diversas etiquetas posibles)
                consumo_diario = serie.isin(["TODOS LOS DÍAS", "DIARIO"]).mean() * 100
                if consumo_diario > 0:  # Solo agregar si hay datos
                    metricas.append((titulos[col_name], "Consumo diario", consumo_diario))
                
                # Calcular porcentaje de no consumo (usando diversas etiquetas posibles)
                no_consumo = serie.isin(["NO CONSUME", "NO CONSUMI ESTE ALIMENTO"]).mean() * 100
                if no_consumo > 0:  # Solo agregar si hay datos
                    metricas.append((titulos[col_name], "No consume", no_consumo))
            
            # Mostrar las 3 métricas más destacadas (o menos si no hay suficientes)
            if metricas:
                metricas_ordenadas = sorted(metricas, key=lambda x: x[2], reverse=True)
                num_metricas = min(3, len(metricas_ordenadas))
                
                for alimento, tipo, valor in metricas_ordenadas[:num_metricas]:
                    delta = "↑" if tipo == "Consumo diario" else "↓"
                    color = "normal" if tipo == "Consumo diario" else "off"
                    st.metric(
                        label=f"{tipo} de {alimento}",
                        value=f"{valor:.1f}%",
                        delta=delta,
                        delta_color=color
                    )
            else:
                st.info("No hay suficientes datos para mostrar métricas destacadas.")
        except Exception as e:
            st.warning(f"No se pudieron calcular las métricas: {e}")
            # Agregar estadísticas de seguridad alimentaria
    st.markdown("---")
    st.markdown("### Indicadores de Seguridad Alimentaria")
    
    try:
        # Crear columnas para mostrar las estadísticas
        col1, col2 = st.columns(2)
        
        with col1:
            # Gráfico de consumo de proteínas (combinado)
            st.markdown("#### Consumo de proteínas animal")
            
            # Calcular frecuencia de consumo diario para las fuentes de proteína
            fuentes_proteina = ['carnes_rojas', 'Pollo', 'Pescado', 'Huevo']
            datos_proteina = []
            
            for proteina in fuentes_proteina:
                if proteina in df.columns:
                    serie = df[proteina]
                elif proteina in posiciones and len(df.columns) > posiciones[proteina]:
                    columnas = list(df.columns)
                    serie = df[columnas[posiciones[proteina]]]
                else:
                    continue
                    
                # Considerar como consumo frecuente: DIARIO, TODOS LOS DÍAS, SEMANAL, etc.
                consumo_frecuente = serie.isin([
                    "TODOS LOS DÍAS", "DIARIO", "DE 2 A 3 VECES A LA SEMANA", 
                    "SEMANAL", "1 VEZ A LA SEMANA"
                ]).mean() * 100
                
                if pd.notna(consumo_frecuente):  # Verificar que el valor no sea NaN
                    datos_proteina.append({
                        "Fuente": titulos[proteina],
                        "Consumo Frecuente (%)": consumo_frecuente
                    })
            
            if datos_proteina:
                proteina_df = pd.DataFrame(datos_proteina)
                
                fig = px.bar(
                    proteina_df, 
                    y="Fuente", 
                    x="Consumo Frecuente (%)",
                    orientation='h',
                    title="Consumo Frecuente de Proteínas",
                    color="Consumo Frecuente (%)",
                    color_continuous_scale=["#FF9800", "#8BC34A", "#2E7D32"]
                )
                
                fig.update_layout(
                    height=300,
                    xaxis_title="Porcentaje de Consumo Frecuente (%)",
                    yaxis_title="",
                    coloraxis_showscale=False
                )
                
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("No hay datos suficientes para mostrar el consumo de proteínas.")
        
        with col2:
            # Gráfico de consumo de frutas/verduras y lácteos
            st.markdown("#### Consumo de alimentos complementarios")
            
            fuentes_complementarias = ['Consumo_frutas_verduras', 'Consumo_lácteos']
            datos_complementarios = []
            
            for alimento in fuentes_complementarias:
                if alimento in df.columns:
                    serie = df[alimento]
                elif alimento in posiciones and len(df.columns) > posiciones[alimento]:
                    columnas = list(df.columns)
                    serie = df[columnas[posiciones[alimento]]]
                else:
                    continue
                    
                # Calcular diferentes tipos de consumo
                consumo_frecuente = serie.isin([
                    "TODOS LOS DÍAS", "DIARIO", "DE 2 A 3 VECES A LA SEMANA", "SEMANAL"
                ]).mean() * 100
                
                consumo_ocasional = serie.isin([
                    "1 VEZ A LA SEMANA", "QUINCENAL", "MENSUAL", "OCASIONAL"
                ]).mean() * 100
                
                no_consume = serie.isin([
                    "NO CONSUME", "NO CONSUMI ESTE ALIMENTO", "NO CONSUMÍ FRUTAS NI VERDURAS"
                ]).mean() * 100
                
                # Solo agregar datos válidos (no NaN)
                if pd.notna(consumo_frecuente):
                    datos_complementarios.append({
                        "Tipo": titulos[alimento], 
                        "Categoría": "Consumo Frecuente", 
                        "Porcentaje": consumo_frecuente
                    })
                
                if pd.notna(consumo_ocasional):
                    datos_complementarios.append({
                        "Tipo": titulos[alimento], 
                        "Categoría": "Consumo Ocasional", 
                        "Porcentaje": consumo_ocasional
                    })
                
                if pd.notna(no_consume):
                    datos_complementarios.append({
                        "Tipo": titulos[alimento], 
                        "Categoría": "No Consume", 
                        "Porcentaje": no_consume
                    })
            
            if datos_complementarios:
                complementarios_df = pd.DataFrame(datos_complementarios)
                
                # Definir colores para las categorías
                colores = {
                    "Consumo Frecuente": "#2E7D32",  # Verde oscuro
                    "Consumo Ocasional": "#FFA000",  # Ámbar
                    "No Consume": "#F44336"          # Rojo
                }
                
                fig = px.bar(
                    complementarios_df,
                    x="Tipo",
                    y="Porcentaje",
                    color="Categoría",
                    barmode="group",
                    title="Patrones de Consumo de Alimentos Complementarios",
                    color_discrete_map=colores
                )
                
                fig.update_layout(
                    height=300,
                    xaxis_title="",
                    yaxis_title="Porcentaje (%)"
                )
                
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("No hay datos suficientes para mostrar el consumo de alimentos complementarios.")
    except Exception as e:
        st.warning(f"Error al generar los gráficos de seguridad alimentaria: {e}")
        # Mostrar medidor de seguridad alimentaria
    try:
        st.markdown("#### Indicador de Seguridad Alimentaria")
        
        # Calcular un "índice" simplificado de seguridad alimentaria basado en el consumo frecuente
        indices = []
        pesos = {
            'carnes_rojas': 0.15,
            'Pollo': 0.20,
            'Pescado': 0.15,
            'Huevo': 0.20,
            'Consumo_frutas_verduras': 0.15,
            'Consumo_lácteos': 0.15
        }
        
        for alimento, peso in pesos.items():
            if alimento in df.columns:
                serie = df[alimento]
            elif alimento in posiciones and len(df.columns) > posiciones[alimento]:
                columnas = list(df.columns)
                serie = df[columnas[posiciones[alimento]]]
            else:
                continue
                
            # Calcular índice ponderado de consumo frecuente
            consumo_frecuente = serie.isin([
                "TODOS LOS DÍAS", "DIARIO", "DE 2 A 3 VECES A LA SEMANA", "SEMANAL"
            ]).mean() * peso
            
            if pd.notna(consumo_frecuente):
                indices.append(consumo_frecuente * 100)  # Convertir a escala 0-100
        
        # Índice general (promedio ponderado) - solo si hay datos
        if indices:
            indice_general = sum(indices)
            
            # Crear un indicador tipo "velocímetro"
            fig = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = indice_general,
                domain = {'x': [0, 1], 'y': [0, 1]},
                title = {'text': "Índice de Seguridad Alimentaria", 'font': {'size': 24}},
                gauge = {
                    'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
                    'bar': {'color': "darkblue"},
                    'bgcolor': "white",
                    'borderwidth': 2,
                    'bordercolor': "gray",
                    'steps': [
                        {'range': [0, 25], 'color': '#F44336'},
                        {'range': [25, 50], 'color': '#FFA000'},
                        {'range': [50, 75], 'color': '#8BC34A'},
                        {'range': [75, 100], 'color': '#2E7D32'}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': 50
                    }
                }
            ))
            
            fig.update_layout(
                height=250,
                margin=dict(l=20, r=20, t=50, b=20),
                paper_bgcolor = "white",
                font = {'color': "darkblue", 'family': "Arial"}
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Leyenda explicativa
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.markdown('<div style="background-color: #F44336; color: white; padding: 10px; border-radius: 5px; text-align: center;">Crítico (0-25%)</div>', unsafe_allow_html=True)
            with col2:
                st.markdown('<div style="background-color: #FFA000; color: white; padding: 10px; border-radius: 5px; text-align: center;">Insuficiente (25-50%)</div>', unsafe_allow_html=True)
            with col3:
                st.markdown('<div style="background-color: #8BC34A; color: white; padding: 10px; border-radius: 5px; text-align: center;">Aceptable (50-75%)</div>', unsafe_allow_html=True)
            with col4:
                st.markdown('<div style="background-color: #2E7D32; color: white; padding: 10px; border-radius: 5px; text-align: center;">Óptimo (75-100%)</div>', unsafe_allow_html=True)
            
            # Interpretación
            st.markdown("""
            **Interpretación**: El índice de seguridad alimentaria es un indicador compuesto que mide la frecuencia de consumo
            de diferentes grupos de alimentos, ponderados según su importancia nutricional. Un valor más alto indica mejor
            seguridad alimentaria en términos de acceso y frecuencia de consumo de alimentos nutritivos.
            """)
        else:
            st.warning("No hay datos suficientes para calcular el índice de seguridad alimentaria.")
    except Exception as e:
        st.warning(f"Error al generar el indicador de seguridad alimentaria: {e}")
        
if __name__ == "__main__":
    st.set_page_config(layout="wide")
    mostrar_pagina_demografia()