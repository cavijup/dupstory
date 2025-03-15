import streamlit as st
from google_connection import load_data
from graficos.grafico_dub import crear_grafico_dub
from graficos.grafico_fechas import crear_grafico_fechas
from utils.svg_utils import mostrar_estadisticas_sexo
from graficos.graficos_adicionales import crear_grafico_pastel, crear_grafico_barras_horizontal, mostrar_graficos_pastel, mostrar_matriz_graficos_barras


def mostrar_pagina_dub():
    """
    Muestra el contenido de la pestaña DUB sin la imagen principal,
    solo con los gráficos y visualizaciones.
    
    Returns:
        DataFrame: Los datos cargados o None si hay un error
    """
    st.header("Datos DUB")
    
    # Mostrar un spinner mientras cargamos los datos
    with st.spinner("Cargando datos desde Google Sheets..."):
        try:
            # Cargar los datos desde la hoja "DUB"
            sheet_id = ""
            df = load_data(sheet_id, "DUB")
            
            if df is not None and not df.empty:
                # Mostrar información básica
                st.success(f"Datos cargados correctamente. Total de filas: {len(df)}")
                
                # 1. PRIMERA FILA: BARRA HORIZONTAL DE PROGRESO ID DUB
                st.markdown("### Primera Fila: Progreso General")
                crear_grafico_dub(df)
                
                # Separador visual
                st.markdown("---")
                
                # 2. SEGUNDA FILA: GRÁFICO DE BARRAS DE FECHA
                st.markdown("### Segunda Fila: Análisis Temporal")
                crear_grafico_fechas(df)
                
                # Separador visual
                st.markdown("---")
                
                # 3. TERCERA FILA: MUESTRA DE DATOS EXPANDIBLE
                
                def crear_analisis_proyeccion(df):
                    """
                    Crea un análisis de proyección para estimar cuándo se alcanzará la meta de 24,000 registros DUB.
                    Excluye fines de semana y días feriados específicos.
                    
                    Args:
                        df: DataFrame con los datos
                    """
                    import pandas as pd
                    from datetime import datetime, timedelta
                    
                    st.markdown("### Tercera Fila: Análisis de Proyección")
                    
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
                        
                        # Calcular registros por día necesarios para terminarlo un mes antes
                        fecha_un_mes_antes = fecha_actual - timedelta(days=30)
                        registros_diarios_meta = registros_faltantes / (dias_calendario - 30)
                        
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
                            
                            # Crear gráfico
                            chart_data = pd.DataFrame({
                                'Registros diarios': registros_grafico['Registros'],
                                'Media móvil (7 días)': registros_grafico['Media móvil']
                            }, index=registros_grafico['Fecha'])
                            
                            st.line_chart(chart_data)
                        
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
                            
                            # Recomendación
                            st.subheader("Para terminar un mes antes")
                            fecha_objetivo = fecha_un_mes_antes.strftime("%d de %B, %Y")
                            st.metric(
                                "Registros diarios necesarios", 
                                f"{registros_diarios_meta:.1f}", 
                                f"{registros_diarios_meta - promedio_diario:.1f} más que el promedio actual"
                            )
                            st.info(f"Para terminar el {fecha_objetivo}, necesitas registrar aproximadamente {int(registros_diarios_meta)} DUB por día laborable.")
                        
                        # Agregar información adicional
                        st.markdown("---")
                        st.caption("Nota: Esta proyección excluye fines de semana y días feriados específicos (24 de marzo y Semana Santa del 14 al 18 de abril).")
                        
                    except Exception as e:
                        st.error(f"Error al generar la proyección: {e}")                           

                # Separador visual
                st.markdown("---")
                
                # 4. CUARTA FILA: VISUALIZACIÓN DE ESTADÍSTICAS POR SEXO
                st.markdown("### Cuarta Fila: Distribución Demográfica")
                
                # Verificar si existe la columna 'Sexo'
                if 'Sexo' not in df.columns:
                    # Si no existe, intentamos buscar la columna AH
                    try:
                        # Renombramos la columna AH a 'Sexo' si existe
                        columnas = list(df.columns)
                        if len(columnas) >= 34:  # AH sería la columna 34 (0-indexado)
                            df['Sexo'] = df[columnas[33]]  # AH sería la columna 34 (0-indexado)
                        else:
                            st.warning("No se encontró la columna en la posición AH. Por favor verifica la estructura de tus datos.")
                    except Exception as e:
                        st.warning(f"No se pudo acceder a la columna de Sexo: {e}")
                
                # Mostrar estadísticas de sexo con imágenes
                mostrar_estadisticas_sexo(df)
                
                # Separador visual
                st.markdown("---")
                
                # 5. QUINTA FILA: GRÁFICOS DE PASTEL PARA IDENTIDAD Y ORIENTACIÓN SEXUAL
                mostrar_graficos_pastel(df)
                
                # Separador visual
                st.markdown("---")
                
                # 6. SEXTA FILA: MATRIZ DE GRÁFICOS DE BARRAS
                # Modificamos el orden de las secciones
                mostrar_matriz_graficos_barras(df)
                
                # Devolver el DataFrame para que pueda ser usado en otras pestañas
                return df
            else:
                st.error("No se pudieron cargar los datos.")
                return None
        except Exception as e:
            st.error(f"Error en la aplicación: {e}")
            return None