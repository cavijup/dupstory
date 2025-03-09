import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

def crear_grafico_fechas(df):
    """
    Crea y muestra el gráfico de conteo de fechas.
    
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
            
            # Convertir a datetime solo para ordenar cronológicamente
            fecha_grouped['FECHA_DT'] = pd.to_datetime(fecha_grouped['FECHA'], errors='coerce')
            fecha_grouped = fecha_grouped.sort_values('FECHA_DT')
            
            # Crear dos columnas (gráfico con 2/3 del ancho, estadísticas con 1/3)
            col_grafico, col_stats = st.columns([2, 1])
            
            # Gráfico en la primera columna (que es más ancha)
            with col_grafico:
                # Crear gráfico de barras con Plotly
                fig = px.bar(
                    fecha_grouped, 
                    x='FECHA',  # Usar la columna original para las etiquetas
                    y='Cantidad',
                    title='Conteo de registros por fecha',
                    color='Cantidad',
                    color_continuous_scale='Blues'
                )
                
                # Mantener el orden cronológico pero con etiquetas originales
                fig.update_layout(
                    xaxis_title='Fecha',
                    xaxis=dict(
                        categoryorder='array',
                        categoryarray=fecha_grouped['FECHA'],
                        tickangle=45
                    ),
                    yaxis_title='Cantidad de registros',
                    plot_bgcolor='white',
                    paper_bgcolor='white',
                    font=dict(color='black'),
                    height=350,  # Tamaño más pequeño
                    margin=dict(l=20, r=20, t=50, b=90)  # Espacio para etiquetas
                )
                
                # Mostrar el gráfico
                st.plotly_chart(fig, use_container_width=True)
            
            # Estadísticas en la segunda columna
            with col_stats:
                st.markdown("### Estadísticas")
                
                # Calcular estadísticas sobre los registros por fecha
                total_registros = fecha_grouped['Cantidad'].sum()
                promedio_diario = fecha_grouped['Cantidad'].mean()
                mediana_diaria = fecha_grouped['Cantidad'].median()
                max_registros = fecha_grouped['Cantidad'].max()
                min_registros = fecha_grouped['Cantidad'].min()
                desviacion_std = fecha_grouped['Cantidad'].std()
                dias_contados = len(fecha_grouped)
                
                # Encontrar el día con más registros
                fecha_max = fecha_grouped.loc[fecha_grouped['Cantidad'].idxmax(), 'FECHA']
                
                # Encontrar el día con menos registros
                fecha_min = fecha_grouped.loc[fecha_grouped['Cantidad'].idxmin(), 'FECHA']
                
                # Crear tabla de estadísticas
                stats_data = [
                    {"Métrica": "Total registros", "Valor": f"{total_registros:,}"},
                    {"Métrica": "Días de ejecucion", "Valor": f"{dias_contados:,}"},
                    {"Métrica": "Promedio diario", "Valor": f"{promedio_diario:.2f}"},
                    
                    {"Métrica": "Máximo diario", "Valor": f"{max_registros:,}"},
                    {"Métrica": "Mínimo diario", "Valor": f"{min_registros:,}"},
                    {"Métrica": "Fecha con más registros", "Valor": fecha_max},
                    {"Métrica": "Fecha con menos registros", "Valor": fecha_min}
                ]
                
                # Mostrar estadísticas como tabla
                st.table(pd.DataFrame(stats_data))
                
        except Exception as e:
            st.warning(f"Error al procesar las fechas: {e}")
            # Crear un gráfico de barras simple como fallback
            st.bar_chart(df['FECHA'].value_counts())
    else:
        st.warning("No se encontró la columna 'FECHA' en los datos")