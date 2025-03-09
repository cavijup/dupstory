import streamlit as st
import pandas as pd
import plotly.express as px

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
            # Contar frecuencia de fechas (no usar value_counts para mantener el formato original)
            fecha_grouped = df.groupby('FECHA').size().reset_index(name='Cantidad')
            
            # Asegurarse de que la fecha está en formato de texto para evitar problemas
            fecha_grouped['FECHA'] = fecha_grouped['FECHA'].astype(str)
            
            # Intentar ordenar si es posible
            try:
                fecha_grouped['FECHA_DT'] = pd.to_datetime(fecha_grouped['FECHA'], errors='coerce')
                fecha_grouped = fecha_grouped.sort_values('FECHA_DT')
                fecha_grouped = fecha_grouped.drop('FECHA_DT', axis=1)
            except:
                # Si no se puede ordenar, mantener el orden original
                pass
            
            # Crear gráfico de barras con Plotly
            fig = px.bar(
                fecha_grouped, 
                x='FECHA', 
                y='Cantidad',
                title='Conteo de registros por fecha',
                color='Cantidad',
                color_continuous_scale='Blues'
            )
            
            fig.update_layout(
                xaxis_title='Fecha',
                yaxis_title='Cantidad de registros',
                plot_bgcolor='white',
                paper_bgcolor='white',
                font=dict(color='black'),
                height=350,
                margin=dict(l=20, r=20, t=50, b=20)
            )
            
            # Rotar las etiquetas del eje X si hay muchas fechas
            if len(fecha_grouped) > 5:
                fig.update_layout(
                    xaxis=dict(
                        tickangle=45,
                        tickmode='array',
                        tickvals=fecha_grouped['FECHA'],
                        ticktext=fecha_grouped['FECHA']
                    )
                )
            
            st.plotly_chart(fig, use_container_width=True)
        except Exception as e:
            st.warning(f"Error al procesar las fechas: {e}")
            # Crear un gráfico de barras simple como fallback
            st.bar_chart(df['FECHA'].value_counts())
    else:
        st.warning("No se encontró la columna 'FECHA' en los datos")