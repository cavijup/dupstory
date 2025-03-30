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
    if 'FECHA' not in df.columns:
        st.warning("No se encontró la columna 'FECHA' en los datos")
        return
    
    st.subheader("Conteo de registros por fecha")
    
    try:
        # Paso 1: Crear copia del dataframe para evitar advertencias
        df_temp = df.copy()
        
        # Paso 2: Agrupar y contar registros por fecha
        fecha_grouped = df_temp.groupby('FECHA').size().reset_index(name='Cantidad')
        
        # Paso 3: Convertir fechas a formato datetime
        # Primero asegurarse que la fecha es texto
        fecha_grouped['FECHA'] = fecha_grouped['FECHA'].astype(str)
        # Especificar formato como DD/MM/YYYY (formato europeo)
        fecha_grouped['FECHA_DT'] = pd.to_datetime(fecha_grouped['FECHA'], format='%d/%m/%Y', errors='coerce')
        
        # Paso 4: Eliminar filas donde la conversión a fecha falló
        fecha_grouped = fecha_grouped.dropna(subset=['FECHA_DT'])
        
        if fecha_grouped.empty:
            st.error("No se pudieron convertir las fechas correctamente. Verifique el formato.")
            return
        
        # Paso 5: Extraer información de año y mes
        fecha_grouped['Año'] = fecha_grouped['FECHA_DT'].dt.year
        fecha_grouped['Mes'] = fecha_grouped['FECHA_DT'].dt.month
        fecha_grouped['NombreMes'] = fecha_grouped['FECHA_DT'].dt.strftime('%B')
        fecha_grouped['AñoMes'] = fecha_grouped['FECHA_DT'].dt.strftime('%Y-%m')
        fecha_grouped['MesAño'] = fecha_grouped['FECHA_DT'].dt.strftime('%B %Y')
        
        # Paso 6: Crear lista de meses disponibles
        meses_disponibles = sorted(fecha_grouped['AñoMes'].unique())
        opciones_texto = []
        
        # Crear nombres legibles para los meses
        for yearmonth in meses_disponibles:
            # Extraer año y mes
            try:
                year, month = yearmonth.split('-')
                # Obtener nombre del mes
                fecha_temp = datetime(int(year), int(month), 1)
                mes_nombre = fecha_temp.strftime('%B %Y')
                opciones_texto.append((yearmonth, mes_nombre))
            except:
                # Si hay error, usar el valor original
                opciones_texto.append((yearmonth, yearmonth))
        
        # Paso 7: Crear filtros
        col_filtro1, col_filtro2 = st.columns([1, 2])
        
        with col_filtro1:
            opciones_display = ["Todos"] + [nombre for _, nombre in opciones_texto]
            opciones_valor = ["Todos"] + [valor for valor, _ in opciones_texto]
            
            # Por defecto, mostrar todos los meses
            mes_index = st.selectbox(
                "Seleccionar mes:",
                options=opciones_display,
                index=0,
                key="selector_mes"
            )
            
            # Convertir selección visual a valor interno
            indice_seleccionado = opciones_display.index(mes_index)
            mes_seleccionado = opciones_valor[indice_seleccionado]
        
        with col_filtro2:
            # Opciones de visualización
            mostrar_promedio = st.checkbox("Mostrar línea de promedio", value=True)
        
        # Paso 8: Filtrar datos según selección
        if mes_seleccionado != "Todos":
            # Obtener año y mes de la selección
            año, mes = mes_seleccionado.split('-')
            # Filtrar por año y mes
            fecha_filtrada = fecha_grouped[
                (fecha_grouped['Año'] == int(año)) & 
                (fecha_grouped['Mes'] == int(mes))
            ]
            titulo_grafico = f'Conteo de registros para {mes_index}'
        else:
            fecha_filtrada = fecha_grouped
            titulo_grafico = 'Conteo de registros por fecha (todos los meses)'
        
        # Paso 9: Mostrar el gráfico y estadísticas
        col_grafico, col_stats = st.columns([2, 1])
        
        # Gráfico en la primera columna
        with col_grafico:
            if fecha_filtrada.empty:
                st.warning(f"No hay datos para el período seleccionado: {mes_index}")
                return
            
            # Ordenar por fecha
            fecha_filtrada = fecha_filtrada.sort_values('FECHA_DT')
            
            # Crear gráfico
            fig = px.bar(
                fecha_filtrada, 
                x='FECHA_DT',
                y='Cantidad',
                title=titulo_grafico,
                color='Cantidad',
                color_continuous_scale='Blues',
                hover_data={
                    'FECHA': True,
                    'FECHA_DT': False,
                    'Cantidad': True
                }
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
            
            # Configurar eje X
            fig.update_xaxes(
                title='Fecha',
                tickformat='%d %b',
                tickangle=45,
                dtick="D1"
            )
            
            # Configuración adicional
            fig.update_layout(
                yaxis_title='Cantidad de registros',
                plot_bgcolor='white',
                paper_bgcolor='white',
                font=dict(color='black'),
                height=400,
                margin=dict(l=20, r=20, t=50, b=90)
            )
            
            # Mostrar gráfico
            st.plotly_chart(fig, use_container_width=True)
        
        # Estadísticas en la segunda columna
        with col_stats:
            st.markdown("### Estadísticas")
            
            # Calcular estadísticas
            total_registros = int(fecha_filtrada['Cantidad'].sum())
            promedio_diario = float(fecha_filtrada['Cantidad'].mean())
            mediana_diaria = float(fecha_filtrada['Cantidad'].median())
            max_registros = int(fecha_filtrada['Cantidad'].max())
            min_registros = int(fecha_filtrada['Cantidad'].min())
            dias_contados = len(fecha_filtrada)
            
            # Dias máximo y mínimo con manejo de errores
            try:
                max_idx = fecha_filtrada['Cantidad'].idxmax()
                fecha_max = fecha_filtrada.loc[max_idx, 'FECHA']
            except:
                fecha_max = "No disponible"
                
            try:
                min_idx = fecha_filtrada['Cantidad'].idxmin()
                fecha_min = fecha_filtrada.loc[min_idx, 'FECHA']
            except:
                fecha_min = "No disponible"
            
            # Crear tabla estadística
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
            
            # Mostrar tabla
            st.table(pd.DataFrame(stats_data))
            
            # Comparativa si está filtrando
            if mes_seleccionado != "Todos":
                st.markdown("### Comparativa")
                total_general = int(fecha_grouped['Cantidad'].sum())
                porcentaje = (total_registros / total_general) * 100
                
                st.metric(
                    label=f"Registros en {mes_index}", 
                    value=f"{total_registros:,}",
                    delta=f"{porcentaje:.1f}% del total"
                )
                
    except Exception as e:
        st.error(f"Error al procesar las fechas: {str(e)}")
        # Mostrar detalles adicionales del error para debugging
        st.warning("Detalles del error para soporte técnico:")
        st.code(str(e))
        
        # Intentar mostrar algo como fallback
        try:
            # Crear un gráfico simple como alternativa
            st.subheader("Vista alternativa (sin procesamiento de fechas)")
            st.bar_chart(df['FECHA'].value_counts().head(30))
        except:
            st.warning("No se pudo crear ni siquiera un gráfico alternativo.")