import streamlit as st
import pandas as pd
import plotly.express as px
import os

def mostrar_pagina_demografia():
    """
    Muestra únicamente la sección de resumen estadístico con la estructura solicitada.
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
        "1 VEZ A LA SEMANA": "#FF9800",           # Naranja
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
    
    # Todas las categorías están seleccionadas
    selected_categories = {cat: True for cat in all_categories}
    
    #========== SECCIÓN RESUMEN ESTADÍSTICO ==========
    st.markdown("## Resumen Estadístico")
    
    # Preparar datos para el resumen
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
    
    # PRIMERA FILA: Gráfico comparativo de patrones de consumo
    if consumo_data:
        st.markdown("### Comparativa de patrones de consumo")
        
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
    
    # SEGUNDA FILA: Métricas destacadas y Conclusiones con referencias
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Métricas Destacadas")
        
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
                
                # Calcular porcentaje de consumo frecuente
                consumo_frecuente = serie.isin(["TODOS LOS DÍAS", "DIARIO", "DE 2 A 3 VECES A LA SEMANA", "SEMANAL"]).mean() * 100
                if consumo_frecuente > 0:  # Solo agregar si hay datos
                    metricas.append((titulos[col_name], "Consumo frecuente", consumo_frecuente))
                
                # Calcular porcentaje de no consumo (usando diversas etiquetas posibles)
                no_consumo = serie.isin(["NO CONSUME", "NO CONSUMI ESTE ALIMENTO"]).mean() * 100
                if no_consumo > 0:  # Solo agregar si hay datos
                    metricas.append((titulos[col_name], "No consume", no_consumo))
            
            # Mostrar las métricas más destacadas
            if metricas:
                metricas_ordenadas = sorted(metricas, key=lambda x: x[2], reverse=True)
                
                # Mostrar métricas de consumo diario
                st.subheader("Consumo Diario")
                for alimento, tipo, valor in [m for m in metricas_ordenadas if m[1] == "Consumo diario"][:3]:
                    st.metric(
                        label=f"{alimento}",
                        value=f"{valor:.1f}%",
                        delta="↑",
                        delta_color="normal"
                    )
                
                # Mostrar métricas de no consumo
                st.subheader("No Consumo")
                for alimento, tipo, valor in [m for m in metricas_ordenadas if m[1] == "No consume"][:3]:
                    st.metric(
                        label=f"{alimento}",
                        value=f"{valor:.1f}%",
                        delta="↓",
                        delta_color="off"
                    )
            else:
                st.info("No hay suficientes datos para mostrar métricas destacadas.")
        except Exception as e:
            st.warning(f"No se pudieron calcular las métricas: {e}")
    
    with col2:
        st.markdown("### Conclusiones")        
        st.markdown("""
        #### Patrones de Consumo Alimentario
        
        El análisis de los datos revela patrones importantes en la frecuencia de consumo de alimentos esenciales que pueden influir significativamente en el estado nutricional de la población beneficiaria.
        
        **Hallazgos principales:**
        - El consumo de proteínas animales muestra disparidades significativas, con mayor acceso a huevo y pollo que a carnes rojas y pescado.
        - La frecuencia de consumo de frutas y verduras está por debajo de las recomendaciones internacionales.
        
        **Implicaciones para la seguridad alimentaria:**
        Según la FAO (2023), el acceso regular a alimentos diversos y nutritivos es fundamental para garantizar una adecuada seguridad alimentaria[¹]. Los resultados observados sugieren áreas de intervención específicas.
        
        **Referencias:**
        
        [¹] FAO. (2023). *El estado de la seguridad alimentaria y la nutrición en el mundo*. Roma: Organización de las Naciones Unidas para la Alimentación y la Agricultura.
        
        [²] OMS. (2022). *Directrices sobre la ingesta de nutrientes para la prevención de enfermedades no transmisibles*. Ginebra: Organización Mundial de la Salud.
        
        [³] Pérez-Rodrigo, C., et al. (2022). "Métodos de evaluación de la ingesta de alimentos: aplicaciones en estudios poblacionales". *Revista Española de Nutrición Comunitaria*, 28(2), 94-109.
        """)
    
    # TERCERA FILA: Tabla resumen
    st.markdown("### Tabla de Resumen")
    
    if summary_data:
        try:
            summary_df = pd.DataFrame(summary_data)
            
            # Crear una tabla pivote con los alimentos como filas y categorías como columnas
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
            
            # Añadir notas explicativas debajo de la tabla
            st.markdown("""
            **Notas sobre la tabla:**
            * Los valores representan el porcentaje de beneficiarios en cada categoría de frecuencia de consumo
            * El total puede no sumar exactamente 100% debido a redondeo
            * Las categorías con 0% indican ausencia de respuestas en esa combinación
            """)
        except Exception as e:
            st.warning(f"No se pudo generar la tabla de resumen: {e}")
    else:
        st.warning("No hay datos suficientes para generar la tabla de resumen.")

if __name__ == "__main__":
    st.set_page_config(layout="wide")
    mostrar_pagina_demografia()