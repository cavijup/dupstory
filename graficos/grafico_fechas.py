import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from datetime import datetime

def crear_grafico_fechas(df):
    """
    Crea y muestra el gráfico de conteo de fechas con filtro por mes.
    
    Args:
        df: DataFrame con los datos
    """
    if 'FECHA' in df.columns:
        st.subheader("Conteo de registros por fecha")
        
        # Intentar convertir y ordenar las fechas
        try:
            # Contar frecuencia de fechas
            fecha_grouped = df.groupby('FECHA').size().reset_index(name='Cantidad')
            
            # Asegurarse de que la fecha está en formato de texto para evitar problemas
            fecha_grouped['FECHA'] = fecha_grouped['FECHA'].astype(str)
            
            # Convertir a datetime para poder extraer mes y año
            fecha_grouped['FECHA_DT'] = pd.to_datetime(fecha_grouped['FECHA'], errors='coerce')
            
            # Crear columnas para año y mes
            fecha_grouped['Año'] = fecha_grouped['FECHA_DT'].dt.year
            fecha_grouped['Mes'] = fecha_grouped['FECHA_DT'].dt.month
            fecha_grouped['NombreMes'] = fecha_grouped['FECHA_DT'].dt.strftime('%B')
            fecha_grouped['AñoMes'] = fecha_grouped['FECHA_DT'].dt.strftime('%Y-%m')
            fecha_grouped['MesAño'] = fecha_grouped['FECHA_DT'].dt.strftime('%B %Y')
            
            # Ordenar cronológicamente
            fecha_grouped = fecha_grouped.sort_values('FECHA_DT')
            
            # Crear filtros para año y mes
            # Obtener lista única de años-meses disponibles
            opciones_mes = sorted(fecha_grouped['MesAño'].unique())
            
            # Crear selector en el sidebar para filtrar por mes
            col_filtro1, col_filtro2 = st.columns([1, 2])
            
            with col_filtro1:
                # Por defecto, mostrar el mes más reciente
                indice_default = len(opciones_mes) - 1 if opciones_mes else 0
                mes_seleccionado = st.selectbox(
                    "Seleccionar mes:",
                    ["Todos"] + list(opciones_mes),
                    index=0
                )
            
            with col_filtro2:
                # Opciones de visualización
                mostrar_promedio = st.checkbox("Mostrar línea de promedio", value=True)
            
            # Filtrar datos según selección
            if mes_seleccionado != "Todos":
                fecha_filtrada = fecha_grouped[fecha_grouped['MesAño'] == mes_seleccionado]
                titulo_grafico = f'Conteo de registros para {mes_seleccionado}'
            else:
                fecha_filtrada = fecha_grouped
                titulo_grafico = 'Conteo de registros por fecha (todos los meses)'
            
            # Crear dos columnas (gráfico con 2/3 del ancho, estadísticas con 1/3)
            col_grafico, col_stats = st.columns([2, 1])
            
            # Gráfico en la primera columna (que es más ancha)
            with col_grafico:
                # Crear gráfico de barras con Plotly
                fig = px.bar(
                    fecha_filtrada, 
                    x='FECHA_DT',  # Usar la fecha datetime para asegurar orden correcto
                    y='Cantidad',
                    title=titulo_grafico,
                    color='Cantidad',
                    color_continuous_scale='Blues',
                    hover_data={'FECHA': True, 'FECHA_DT': False}  # Mostrar fecha original en hover
                )
                
                # Añadir línea de promedio si está seleccionado
                if mostrar_promedio:
                    promedio = fecha_filtrada['Cantidad'].mean()
                    fig.add_hline(
                        y=promedio,
                        line_dash="dash",
                        line_color="red",
                        annotation_text=f"Promedio: {promedio:.1f}",
                        annotation_position="top right"
                    )
                
                # Configurar formato de fechas en eje X
                fig.update_xaxes(
                    title='Fecha',
                    tickformat='%d %b',  # Formato: día mes
                    tickangle=45,
                    dtick="D1"  # Mostrar cada día
                )
                
                fig.update_layout(
                    yaxis_title='Cantidad de registros',
                    plot_bgcolor='white',
                    paper_bgcolor='white',
                    font=dict(color='black'),
                    height=400,  # Altura ligeramente mayor
                    margin=dict(l=20, r=20, t=50, b=90)  # Espacio para etiquetas
                )
                
                # Mostrar el gráfico
                st.plotly_chart(fig, use_container_width=True)
            
            # Estadísticas en la segunda columna
            with col_stats:
                st.markdown("### Estadísticas")
                
                # Calcular estadísticas sobre los registros por fecha
                if not fecha_filtrada.empty:
                    total_registros = fecha_filtrada['Cantidad'].sum()
                    promedio_diario = fecha_filtrada['Cantidad'].mean()
                    mediana_diaria = fecha_filtrada['Cantidad'].median()
                    max_registros = fecha_filtrada['Cantidad'].max()
                    min_registros = fecha_filtrada['Cantidad'].min()
                    desviacion_std = fecha_filtrada['Cantidad'].std()
                    dias_contados = len(fecha_filtrada)
                    
                    # Encontrar el día con más registros
                    fecha_max = fecha_filtrada.loc[fecha_filtrada['Cantidad'].idxmax(), 'FECHA']
                    
                    # Encontrar el día con menos registros
                    fecha_min = fecha_filtrada.loc[fecha_filtrada['Cantidad'].idxmin(), 'FECHA']
                    
                    # Crear tabla de estadísticas
                    stats_data = [
                        {"Métrica": "Total registros", "Valor": f"{total_registros:,}"},
                        {"Métrica": "Días de registro", "Valor": f"{dias_contados:,}"},
                        {"Métrica": "Promedio diario", "Valor": f"{promedio_diario:.2f}"},
                        {"Métrica": "Mediana diaria", "Valor": f"{mediana_diaria:.2f}"},
                        {"Métrica": "Máximo diario", "Valor": f"{max_registros:,}"},
                        {"Métrica": "Mínimo diario", "Valor": f"{min_registros:,}"},
                        {"Métrica": "Fecha con más registros", "Valor": fecha_max},
                        {"Métrica": "Fecha con menos registros", "Valor": fecha_min}
                    ]
                    
                    # Mostrar estadísticas como tabla
                    st.table(pd.DataFrame(stats_data))
                    
                    # Si está filtrando, mostrar comparativa con totales
                    if mes_seleccionado != "Todos":
                        st.markdown("### Comparativa")
                        total_general = fecha_grouped['Cantidad'].sum()
                        porcentaje = (total_registros / total_general) * 100
                        
                        st.metric(
                            label=f"Registros en {mes_seleccionado}", 
                            value=f"{total_registros:,}",
                            delta=f"{porcentaje:.1f}% del total"
                        )
                else:
                    st.warning("No hay datos para el periodo seleccionado.")
                
        except Exception as e:
            st.warning(f"Error al procesar las fechas: {e}")
            # Crear un gráfico de barras simple como fallback
            st.bar_chart(df['FECHA'].value_counts())
    else:
        st.warning("No se encontró la columna 'FECHA' en los datos")