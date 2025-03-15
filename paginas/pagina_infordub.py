import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import plotly.express as px
from google_connection import load_data
from graficos.grafico_dub import crear_grafico_dub
from graficos.grafico_fechas import crear_grafico_fechas


def crear_analisis_proyeccion(df):
    """
    Crea un análisis de proyección para estimar cuándo se alcanzará la meta de 24,000 registros DUB.
    Excluye fines de semana y días feriados específicos.
    
    Args:
        df: DataFrame con los datos
    """
    st.markdown("### Análisis de Proyección")
    
    # Verificar si existe la columna necesaria
    if 'FECHA' not in df.columns or 'ID DUB' not in df.columns:
        st.warning("No se encontraron las columnas 'FECHA' o 'ID DUB' necesarias para la proyección")
        return
    
    try:
        # Convertir fechas a datetime
        df['FECHA_DT'] = pd.to_datetime(df['FECHA'], errors='coerce')
        
        # Contar registros únicos por fecha
        registros_por_dia = df.groupby('FECHA_DT')['ID DUB'].nunique().reset_index()
        registros_por_dia.columns = ['Fecha', 'Registros']
        
        # Calcular estadísticas
        total_registros = df['ID DUB'].nunique()
        meta = 24000
        registros_faltantes = meta - total_registros
        promedio_diario = registros_por_dia['Registros'].mean()
        
        # Calcular días necesarios (sin contar fines de semana y feriados)
        dias_laborables_necesarios = int(registros_faltantes / promedio_diario) + 1
        
        # Definir días feriados específicos
        feriados = [
            pd.Timestamp('2025-03-24'),  # 24 de marzo
            pd.Timestamp('2025-04-14'),  # Lunes Santo
            pd.Timestamp('2025-04-15'),  # Martes Santo
            pd.Timestamp('2025-04-16'),  # Miércoles Santo
            pd.Timestamp('2025-04-17'),  # Jueves Santo
            pd.Timestamp('2025-04-18'),  # Viernes Santo
        ]
        
        # Calcular fecha de finalización excluyendo fines de semana y feriados
        fecha_actual = datetime.now()
        dias_agregados = 0
        dias_calendario = 0
        
        while dias_agregados < dias_laborables_necesarios:
            fecha_actual += timedelta(days=1)
            dias_calendario += 1
            
            # Verificar si es día hábil (no fin de semana ni feriado)
            if fecha_actual.weekday() < 5 and fecha_actual.date() not in [f.date() for f in feriados]:
                dias_agregados += 1
        
        # Mostrar resultados
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Estado Actual")
            st.metric("Registros actuales", f"{total_registros:,}", f"Faltan {registros_faltantes:,}")
            st.metric("Promedio diario actual", f"{promedio_diario:.1f} registros/día")
            
            # Gráfico de línea de registros por día
            st.subheader("Tendencia de registros diarios")
            
            # Asegurar que las fechas estén ordenadas
            registros_grafico = registros_por_dia.sort_values('Fecha')
            
            # Calcular media móvil de 7 días
            registros_grafico['Media móvil'] = registros_grafico['Registros'].rolling(window=7, min_periods=1).mean()
            
            # Crear gráfico con Plotly
            fig = px.line(
                registros_grafico, 
                x='Fecha', 
                y=['Registros', 'Media móvil'],
                title='Tendencia de registros diarios',
                labels={'value': 'Cantidad', 'variable': 'Serie'},
                color_discrete_sequence=['#1f77b4', '#ff7f0e']
            )
            
            # Personalizar diseño
            fig.update_layout(
                xaxis_title='Fecha',
                yaxis_title='Cantidad de registros',
                legend_title='',
                hovermode='x unified'
            )
            
            # Mostrar el gráfico
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("Proyección")
            st.metric(
                "Días laborables necesarios", 
                f"{dias_laborables_necesarios}", 
                f"{dias_calendario} días calendario"
            )
            
            # Formatear fecha
            fecha_estimada = fecha_actual.strftime("%d de %B, %Y")
            st.metric("Fecha estimada de finalización", fecha_estimada)
            
            # Reemplazar la sección "Para terminar un mes antes" con "Para terminar antes del 25 de abril"
            fecha_limite = pd.Timestamp('2025-04-25')
            dias_hasta_limite = (fecha_limite - datetime.now().date()).days
            dias_laborables_hasta_limite = 0
            fecha_contador = datetime.now().date()

            # Contar días laborables hasta la fecha límite
            for _ in range(dias_hasta_limite):
                fecha_contador += timedelta(days=1)
                # Verificar si es día hábil (no fin de semana ni feriado)
                if fecha_contador.weekday() < 5 and fecha_contador not in [f.date() for f in feriados]:
                    dias_laborables_hasta_limite += 1

            # Calcular registros diarios necesarios para cumplir la meta antes de la fecha límite
            registros_diarios_meta = registros_faltantes / dias_laborables_hasta_limite if dias_laborables_hasta_limite > 0 else 0

            # Recomendación
            st.subheader("Para terminar antes del 25 de abril")
            st.metric(
                "Registros diarios necesarios", 
                f"{registros_diarios_meta:.1f}", 
                f"{registros_diarios_meta - promedio_diario:.1f} más que el promedio actual"
            )
            st.info(f"Para completar la meta antes del 25 de abril de 2025 (fecha límite), necesitas registrar aproximadamente {int(registros_diarios_meta)} IDs DUB por día laborable.")
        
        # Agregar información adicional
        st.markdown("---")
        st.caption("Nota: Esta proyección excluye fines de semana y días feriados específicos (24 de marzo y Semana Santa del 14 al 18 de abril).")
        
    except Exception as e:
        st.error(f"Error al generar la proyección: {e}")


def mostrar_pagina_infordub():
    """
    Muestra la información general sobre progreso DUB, análisis temporal y proyección
    
    Returns:
        DataFrame: Los datos cargados o None si hay un error
    """
    st.header("Información DUB")
    
    # Verificar si hay datos cargados en la sesión
    if 'df' in st.session_state:
        df = st.session_state.df
        st.success(f"Usando datos cargados. Total de filas: {len(df)}")
    else:
        # Si no hay datos cargados, intentar cargarlos
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
                    return None
            except Exception as e:
                st.error(f"Error en la aplicación: {e}")
                return None
    
    # 1. PROGRESO GENERAL DUB
    st.markdown("### Progreso General")
    crear_grafico_dub(df)
    
    # Separador visual
    st.markdown("---")
    
    # 2. ANÁLISIS TEMPORAL
    st.markdown("### Análisis Temporal")
    crear_grafico_fechas(df)
    
    # Separador visual
    st.markdown("---")
    
    # 3. ANÁLISIS DE PROYECCIÓN
    crear_analisis_proyeccion(df)

    return df