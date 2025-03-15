import streamlit as st
import pandas as pd
import plotly.express as px
import re
import numpy as np
from google_connection import load_data

def extraer_coordenadas(ubicacion):
    """
    Extrae coordenadas de latitud y longitud de una cadena de texto.
    
    Args:
        ubicacion: String con coordenadas en formato "(latitud, longitud)"
    
    Returns:
        Tupla (latitud, longitud) o (None, None) si no se puede extraer
    """
    if pd.isna(ubicacion) or not isinstance(ubicacion, str):
        return None, None
    
    # Intentar extraer coordenadas con regex
    patron = r"\(?(-?\d+\.?\d*)[,\s]+(-?\d+\.?\d*)\)?"
    match = re.search(patron, ubicacion)
    
    if match:
        try:
            lat = float(match.group(1))
            lon = float(match.group(2))
            
            # Validar que las coordenadas estén en rangos válidos
            if -90 <= lat <= 90 and -180 <= lon <= 180:
                return lat, lon
        except ValueError:
            pass
    
    return None, None

def limpiar_nombre_comedor(nombre):
    """
    Limpia y estandariza el nombre del comedor.
    
    Args:
        nombre: Nombre original del comedor
    
    Returns:
        Nombre limpio del comedor
    """
    if pd.isna(nombre) or not isinstance(nombre, str):
        return "Desconocido"
    
    # Eliminar espacios extras y convertir a título
    nombre_limpio = nombre.strip().title()
    
    # Si está vacío, devolver "Desconocido"
    return nombre_limpio if nombre_limpio else "Desconocido"

def cargar_info_comedores():
    """
    Carga la información de la tabla COMEDORES.
    
    Returns:
        DataFrame con la información de comedores y sus cupos
    """
    try:
        # Usar el mismo sheet_id que para la tabla DUB
        sheet_id = "1haZINioOFe4WTL2G9FzsYt0p4-8uJ5WKbukexBYhx_o"
        df_comedores = load_data(sheet_id, "COMEDORES")
        
        if df_comedores is not None and not df_comedores.empty:
            # Verificar si tiene las columnas correctas, o buscar por posición
            if 'Nombre_comedor' not in df_comedores.columns and len(df_comedores.columns) > 1:
                # Suponemos que la columna B (índice 1) contiene los nombres
                df_comedores['Nombre_comedor'] = df_comedores.iloc[:, 1]
            
            if 'Cupos' not in df_comedores.columns and len(df_comedores.columns) > 3:
                # Suponemos que la columna D (índice 3) contiene los cupos
                df_comedores['Cupos'] = df_comedores.iloc[:, 3]
                
                # Convertir cupos a numérico
                df_comedores['Cupos'] = pd.to_numeric(df_comedores['Cupos'], errors='coerce')
            
            # Limpiar nombres de comedores para facilitar la comparación
            df_comedores['Nombre_comedor_limpio'] = df_comedores['Nombre_comedor'].apply(limpiar_nombre_comedor)
            
            st.success(f"Información de comedores cargada: {len(df_comedores)} comedores con información de cupos")
            return df_comedores
        else:
            st.warning("No se pudo cargar la información de COMEDORES")
            return None
    except Exception as e:
        st.warning(f"Error al cargar información de COMEDORES: {e}")
        return None

def crear_mapa(df):
    """
    Crea y muestra un mapa con las ubicaciones de los comedores.
    
    Args:
        df: DataFrame con los datos
    """
    st.header("Mapa de Ubicaciones")
    
    # Crear una copia para no modificar el original
    df_temp = df.copy()
    
    # Cargar información de comedores y cupos
    df_comedores = cargar_info_comedores()
    if df_comedores is not None:
        st.success(f"Información de comedores cargada: {len(df_comedores)} comedores con información de cupos")
    
    # Verificar si existen las columnas necesarias
    columnas_requeridas = ["UBICACION_PREDEFINIDA", "Nombre_comedor", "Se_reconoce_como"]
    columnas_faltantes = [col for col in columnas_requeridas if col not in df_temp.columns]
    
    # Si faltan columnas, buscar por posición
    if columnas_faltantes:
        st.warning(f"Columnas faltantes: {', '.join(columnas_faltantes)}. Intentando ubicar por posición...")
        
        columnas = list(df_temp.columns)
        
        # Asignar por posición si es posible
        if "UBICACION_PREDEFINIDA" not in df_temp.columns and len(columnas) > 105:  # DA = posición 105
            df_temp["UBICACION_PREDEFINIDA"] = df_temp[columnas[105]]
            st.success("Columna 'UBICACION_PREDEFINIDA' asignada por posición.")
        
        if "Nombre_comedor" not in df_temp.columns and len(columnas) > 100:  # CX = aproximadamente posición 100
            df_temp["Nombre_comedor"] = df_temp[columnas[100]]
            st.success("Columna 'Nombre_comedor' asignada por posición.")
        
        if "Se_reconoce_como" not in df_temp.columns and len(columnas) > 37:  # AL = posición 37
            df_temp["Se_reconoce_como"] = df_temp[columnas[37]]
            st.success("Columna 'Se_reconoce_como' asignada por posición.")
    
    # Verificar nuevamente si existen las columnas necesarias
    if "UBICACION_PREDEFINIDA" not in df_temp.columns:
        st.error("No se pudo encontrar la columna de ubicación. No se puede crear el mapa.")
        return
    
    if "Nombre_comedor" not in df_temp.columns:
        st.warning("No se pudo encontrar la columna de nombre de comedor. Se usará 'Desconocido'.")
        df_temp["Nombre_comedor"] = "Desconocido"
    
    if "Se_reconoce_como" not in df_temp.columns:
        st.warning("No se pudo encontrar la columna de reconocimiento étnico. No se mostrará esta información.")
        df_temp["Se_reconoce_como"] = "No especificado"
    
    # Crear columnas para latitud y longitud
    df_temp['lat'] = None
    df_temp['lon'] = None
    
    # Extraer coordenadas
    for idx, row in df_temp.iterrows():
        lat, lon = extraer_coordenadas(row['UBICACION_PREDEFINIDA'])
        df_temp.at[idx, 'lat'] = lat
        df_temp.at[idx, 'lon'] = lon
    
    # Limpiar nombres de comedores
    df_temp['Nombre_comedor_limpio'] = df_temp['Nombre_comedor'].apply(limpiar_nombre_comedor)
    
    # Filtrar filas con coordenadas válidas
    df_map = df_temp.dropna(subset=['lat', 'lon']).copy()
    
    if df_map.empty:
        st.error("No se encontraron coordenadas válidas en los datos. Por favor verifica el formato de la columna 'UBICACION_PREDEFINIDA'.")
        
        # Mostrar ejemplos de los valores de ubicación para ayudar a depurar
        st.subheader("Ejemplos de valores en la columna 'UBICACION_PREDEFINIDA':")
        ejemplos = df_temp['UBICACION_PREDEFINIDA'].dropna().sample(min(5, len(df_temp))).tolist()
        for i, ejemplo in enumerate(ejemplos):
            st.code(f"Ejemplo {i+1}: {ejemplo}")
        
        return
    
    # Agrupar datos por comedor - CORREGIDO PARA EVITAR ERROR DE COLUMNA DUPLICADA
    grouped_data = []
    
    for (comedor, lat, lon), group in df_map.groupby(['Nombre_comedor_limpio', 'lat', 'lon']):
        # Contar distribución étnica
        etnia_counts = group['Se_reconoce_como'].value_counts().to_dict()
        
        # Buscar cupos para este comedor si la información está disponible
        cupos = None
        porcentaje_cupos = None
        
        if df_comedores is not None:
            # Buscar coincidencia por nombre
            comedores_match = df_comedores[df_comedores['Nombre_comedor_limpio'] == comedor]
            if not comedores_match.empty:
                # Tomar el primer match si hay varios
                cupos = comedores_match['Cupos'].iloc[0]
                if pd.notna(cupos) and cupos > 0:
                    porcentaje_cupos = (len(group) / cupos) * 100
        
        # Agregar a la lista de resultados
        grouped_data.append({
            'Comedor': comedor,
            'lat': lat,
            'lon': lon,
            'Conteo': len(group),
            'Distribución_étnica': etnia_counts,
            'Cupos': cupos,
            'Porcentaje_cupos': porcentaje_cupos
        })
    
    # Crear dataframe con los datos agrupados
    agrupado = pd.DataFrame(grouped_data)
    
    # Crear texto para hover con distribución étnica y porcentaje de cupos
    def crear_texto_hover(row):
        texto = f"<b>{row['Comedor']}</b><br>"
        texto += f"Registros: {row['Conteo']}<br>"
        
        # Agregar información de cupos si está disponible
        if pd.notna(row['Cupos']):
            texto += f"Cupos disponibles: {int(row['Cupos'])}<br>"
            if pd.notna(row['Porcentaje_cupos']):
                texto += f"Porcentaje ocupado: {row['Porcentaje_cupos']:.1f}%<br>"
        
        texto += "<br><b>Distribución étnica:</b><br>"
        
        # Ordenar distribución étnica de mayor a menor
        distribucion = row['Distribución_étnica']
        if distribucion:
            for etnia, conteo in sorted(distribucion.items(), key=lambda x: x[1], reverse=True):
                if pd.notna(etnia) and str(etnia).strip():
                    porcentaje = (conteo / row['Conteo']) * 100
                    texto += f"{etnia}: {conteo} ({porcentaje:.1f}%)<br>"
        
        return texto
    
    agrupado['hover_text'] = agrupado.apply(crear_texto_hover, axis=1)
    
    # Crear filtros en el sidebar
    st.sidebar.header("Filtros del Mapa")
    
    # Filtrar por nombre de comedor
    comedores_unicos = sorted(agrupado['Comedor'].unique())
    comedores_seleccionados = st.sidebar.multiselect(
        "Filtrar por comedores:", 
        comedores_unicos,
        default=comedores_unicos 
    )
    
    # Filtro adicional para mostrar solo comedores con información de cupos
    if df_comedores is not None:
        mostrar_solo_con_cupos = st.sidebar.checkbox("Mostrar solo comedores con información de cupos", value=False)
        if mostrar_solo_con_cupos:
            agrupado = agrupado.dropna(subset=['Cupos'])
    
    # Aplicar filtros
    if comedores_seleccionados:
        agrupado_filtrado = agrupado[agrupado['Comedor'].isin(comedores_seleccionados)]
    else:
        agrupado_filtrado = agrupado
    
    # Crear mapa con Plotly
    fig = px.scatter_mapbox(
        agrupado_filtrado,
        lat="lat",
        lon="lon",
        size="Conteo",
        hover_name="Comedor",
        hover_data={"lat": False, "lon": False, "Conteo": False, "hover_text": True},
        custom_data=["hover_text"],
        color="Porcentaje_cupos" if "Porcentaje_cupos" in agrupado_filtrado.columns else "Conteo",
        color_continuous_scale="RdYlGn" if "Porcentaje_cupos" in agrupado_filtrado.columns else "Viridis",
        size_max=25,
        zoom=11,
        title="Mapa de Comedores por Ubicación"
    )
    
    # Configurar el hover para mostrar la información étnica
    fig.update_traces(
        hovertemplate="%{customdata[0]}",
    )
    
    # Cambiar el estilo del mapa
    fig.update_layout(
        mapbox_style="carto-positron",
        mapbox=dict(
            center=dict(
                lat=agrupado_filtrado["lat"].mean() if not agrupado_filtrado.empty else 4.6097,
                lon=agrupado_filtrado["lon"].mean() if not agrupado_filtrado.empty else -74.0817
            ),
        ),
        height=700,
        margin={"r": 0, "t": 50, "l": 0, "b": 0},
        coloraxis_colorbar=dict(
            title="% de Cupos" if "Porcentaje_cupos" in agrupado_filtrado.columns else "Registros"
        )
    )
    
    # Mostrar estadísticas generales
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label="Total de Ubicaciones",
            value=len(agrupado_filtrado)
        )
    
    with col2:
        st.metric(
            label="Total de Registros",
            value=f"{agrupado_filtrado['Conteo'].sum():,}"
        )
    
    with col3:
        if 'Porcentaje_cupos' in agrupado_filtrado.columns and not agrupado_filtrado['Porcentaje_cupos'].isna().all():
            promedio_porcentaje = agrupado_filtrado['Porcentaje_cupos'].mean()
            st.metric(
                label="Promedio % de Cupos",
                value=f"{promedio_porcentaje:.1f}%"
            )
        else:
            promedio = agrupado_filtrado['Conteo'].mean() if not agrupado_filtrado.empty else 0
            st.metric(
                label="Promedio por Ubicación",
                value=f"{promedio:.1f}"
            )
    
    # Mostrar mapa
    st.plotly_chart(fig, use_container_width=True)
    
    # Mostrar tabla de resumen
    st.subheader("Resumen de Ubicaciones")
    
    # Preparar tabla resumida para mostrar
    if not agrupado_filtrado.empty:
        # Seleccionar columnas para la tabla
        columnas_tabla = ['Comedor', 'Conteo']
        
        # Agregar columnas de cupos si están disponibles
        if 'Cupos' in agrupado_filtrado.columns and not agrupado_filtrado['Cupos'].isna().all():
            columnas_tabla.extend(['Cupos', 'Porcentaje_cupos'])
        
        tabla_resumen = agrupado_filtrado[columnas_tabla].copy()
        
        # Calcular porcentaje del total
        tabla_resumen['Porcentaje_del_total'] = (tabla_resumen['Conteo'] / tabla_resumen['Conteo'].sum() * 100).round(2)
        
        # Formatear porcentajes
        if 'Porcentaje_cupos' in tabla_resumen.columns:
            tabla_resumen['Porcentaje_cupos'] = tabla_resumen['Porcentaje_cupos'].apply(
                lambda x: f"{x:.1f}%" if pd.notna(x) else "N/A"
            )
        
        tabla_resumen['Porcentaje_del_total'] = tabla_resumen['Porcentaje_del_total'].astype(str) + '%'
        
        # Formatear números con separador de miles
        tabla_resumen['Conteo'] = tabla_resumen['Conteo'].apply(lambda x: f"{x:,}")
        
        if 'Cupos' in tabla_resumen.columns:
            tabla_resumen['Cupos'] = tabla_resumen['Cupos'].apply(
                lambda x: f"{int(x):,}" if pd.notna(x) else "N/A"
            )
        
        # Ordenar por conteo descendente
        tabla_resumen = tabla_resumen.sort_values('Conteo', ascending=False, key=lambda x: pd.to_numeric(x.str.replace(',', ''), errors='coerce'))
        
        # Renombrar columnas para mejor visualización
        nuevos_nombres = {
            'Comedor': 'Comedor',
            'Conteo': 'Registros',
            'Cupos': 'Cupos Totales',
            'Porcentaje_cupos': '% de Cupos Ocupados',
            'Porcentaje_del_total': '% del Total de Registros'
        }
        
        tabla_resumen = tabla_resumen.rename(columns=nuevos_nombres)
        
        # Mostrar tabla
        st.dataframe(tabla_resumen, use_container_width=True)
        
        # Mostrar información adicional si hay datos de cupos
        if 'Cupos Totales' in tabla_resumen.columns:
            # Contar comedores con y sin información
            total_comedores = len(tabla_resumen)
            comedores_con_info = tabla_resumen['Cupos Totales'].apply(lambda x: x != "N/A").sum()
            
            st.info(f"{comedores_con_info} de {total_comedores} comedores tienen información de cupos disponibles ({comedores_con_info/total_comedores*100:.1f}%)")
    else:
        st.info("No hay datos para mostrar en la tabla de resumen.")

def mostrar_mapa():
    """
    Función principal para mostrar la página del mapa
    """
    st.title("Mapa de Comedores")
    
    # Verificar si hay datos cargados en la sesión
    if 'df' in st.session_state:
        crear_mapa(st.session_state.df)
    else:
        st.warning("No hay datos cargados. Por favor, carga los datos primero desde la pestaña DUB.")
        
        # Botón para cargar datos de demostración (solo para pruebas)
        if st.button("Cargar datos de demostración"):
            # Datos de demostración con coordenadas ficticias
            data = {
                'UBICACION_PREDEFINIDA': ['(4.6097, -74.0817)', '(4.6261, -74.0632)', '(4.5981, -74.0758)'],
                'Nombre_comedor': ['Comedor A', 'Comedor B', 'Comedor C'],
                'Se_reconoce_como': ['INDÍGENA', 'AFRODESCENDIENTE', 'MESTIZO']
            }
            demo_df = pd.DataFrame(data)
            crear_mapa(demo_df)

if __name__ == "__main__":
    st.set_page_config(layout="wide")
    mostrar_mapa()