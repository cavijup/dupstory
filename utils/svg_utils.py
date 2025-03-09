import streamlit as st
import pandas as pd
import os

def mostrar_estadisticas_sexo(df):
    """
    Muestra estadísticas de sexo con imágenes locales.
    
    Args:
        df: DataFrame con los datos que contiene la columna 'Sexo'
    """
    # Verificar si existe la columna Sexo
    if 'Sexo' not in df.columns:
        st.warning("No se encontró la columna 'Sexo' en los datos")
        return
    
    # Contar valores de sexo
    conteo_sexo = df['Sexo'].value_counts()
    total = len(df)
    
    # Crear título de la sección
    st.subheader("Distribución por Sexo")
    
    # Rutas a las imágenes locales (ajusta según tu estructura de carpetas)
    ruta_imagenes = "imagenes"  # O "imagenes" según cómo hayas nombrado la carpeta
    img_hombre = os.path.join(ruta_imagenes, "hombre.png")
    img_mujer = os.path.join(ruta_imagenes, "mujer.png")
    img_intersexual = os.path.join(ruta_imagenes, "interesexual.png")
    
    # Crear diseño de cuatro columnas
    col1, col2, col3, col4 = st.columns([1, 1, 1, 2])
    
    # En la primera columna mostramos la imagen de hombre y sus estadísticas
    with col1:
        st.markdown("#### Hombres")
        # Mostrar imagen local
        st.image(img_hombre, width=120)
        
        # Calcular cantidad y porcentaje de hombres
        hombres = conteo_sexo.get('M', 0) + conteo_sexo.get('MASCULINO', 0) + conteo_sexo.get('HOMBRE', 0)
        porcentaje_hombres = (hombres / total) * 100 if total > 0 else 0
        
        # Mostrar estadísticas de hombres
        st.markdown(f"<div style='text-align: center; font-weight: bold;'>{hombres:,}</div>", unsafe_allow_html=True)
        st.markdown(f"<div style='text-align: center;'>({porcentaje_hombres:.1f}%)</div>", unsafe_allow_html=True)
    
    # En la segunda columna mostramos la imagen de mujer y sus estadísticas
    with col2:
        st.markdown("#### Mujeres")
        # Mostrar imagen local
        st.image(img_mujer, width=120)
        
        # Calcular cantidad y porcentaje de mujeres
        mujeres = conteo_sexo.get('F', 0) + conteo_sexo.get('FEMENINO', 0) + conteo_sexo.get('MUJER', 0)
        porcentaje_mujeres = (mujeres / total) * 100 if total > 0 else 0
        
        # Mostrar estadísticas de mujeres
        st.markdown(f"<div style='text-align: center; font-weight: bold;'>{mujeres:,}</div>", unsafe_allow_html=True)
        st.markdown(f"<div style='text-align: center;'>({porcentaje_mujeres:.1f}%)</div>", unsafe_allow_html=True)
    
    # En la tercera columna mostramos la imagen de intersexual y sus estadísticas
    with col3:
        st.markdown("#### Otros")
        # Mostrar imagen local
        st.image(img_intersexual, width=120)
        
        # Calcular cantidad y porcentaje de otros
        otros = total - (hombres + mujeres)
        porcentaje_otros = (otros / total) * 100 if total > 0 else 0
        
        # Mostrar estadísticas de otros
        st.markdown(f"<div style='text-align: center; font-weight: bold;'>{otros:,}</div>", unsafe_allow_html=True)
        st.markdown(f"<div style='text-align: center;'>({porcentaje_otros:.1f}%)</div>", unsafe_allow_html=True)
    
    # En la cuarta columna mostramos una tabla con todas las estadísticas
    with col4:
        st.markdown("### Detalles por Sexo")
        
        # Crear tabla con todos los valores
        tabla_datos = []
        for sexo, count in conteo_sexo.items():
            porcentaje = (count / total) * 100 if total > 0 else 0
            tabla_datos.append({
                "Categoría": sexo,
                "Cantidad": f"{count:,}",
                "Porcentaje": f"{porcentaje:.1f}%"
            })
        
        # Agregar fila de total
        tabla_datos.append({
            "Categoría": "TOTAL",
            "Cantidad": f"{total:,}",
            "Porcentaje": "100.0%"
        })
        
        # Mostrar tabla
        st.table(tabla_datos)