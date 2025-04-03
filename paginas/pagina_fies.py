import streamlit as st
import pandas as pd
import os

def mostrar_pagina_fies():
    """
    Muestra el contenido de la pestaña FIES
    """
    # Verificar si existen las carpetas de imágenes
    ruta_imagenes = "imagenes"
    
    # Título principal con imagen
    col_titulo1, col_titulo2 = st.columns([3, 1])
    
    with col_titulo1:
        st.header("APLICACIÓN DE LA ESCALA DE EXPERIENCIA DE INSEGURIDAD ALIMENTARIA (FIES)")
    
    with col_titulo2:
        # Cargar imagen de Hambre Cero
        try:
            st.image(os.path.join(ruta_imagenes, "hambre cero.png"), width=150)
        except:
            st.warning("No se pudo cargar la imagen 'hambre cero.png'")
    
    # Primera fila de contenido (3 columnas)
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        La FIES es una herramienta utilizada para estimar la gravedad de la inseguridad alimentaria de individuos u hogares. 
        Las ocho preguntas del módulo están orientadas a revelar condiciones que cubren un rango de severidad y el protocolo 
        analítico de la FIES hace posible transformar la información cualitativa recopilada (respuestas "sí / no") en 
        medidas cuantitativas de la severidad de la situación de inseguridad alimentaria, lo que permite categorizar a los 
        encuestados en clases de inseguridad alimentaria moderada y grave para posteriormente generar las estimaciones.
        """)
    
    with col2:
        # Cargar imagen de 8 preguntas
        try:
            st.image(os.path.join(ruta_imagenes, "8 preguntas.png"), width=300)
        except:
            st.warning("No se pudo cargar la imagen '8 preguntas.png'")
    
    with col3:
        st.markdown("""
        El significado de la seguridad alimentaria, inseguridad alimentaria moderada e inseguridad alimentaria grave, 
        y cada categoría se muestra como una proporción de la población total.
        """)
        
        # Cargar imagen de niveles de inseguridad
        try:
            st.image(os.path.join(ruta_imagenes, "niveles de inseguridad.png"), width=300)
        except:
            st.warning("No se pudo cargar la imagen 'niveles de inseguridad.png'")
    
    # Separador
    st.markdown("---")
    
    # Segunda fila - Parámetros del encuestado
    st.subheader("Parámetros del encuestado")
    
    st.markdown("""
    El puntaje bruto de un encuestado es la cantidad de respuestas afirmativas dadas a las ocho preguntas de la FIES, 
    constituyendo un número entero con un valor entre 0 y 8, representando en sí misma, una medida ordinal e intuitiva 
    de la situación de inseguridad alimentaria. Por lo cual, aquellos encuestados con puntajes brutos más altos serán 
    los que estén experimentando situaciones relacionadas con dificultades en el acceso a los alimentos. En la ilustración 1 
    se observa que el 23% respondieron "No" a las ocho preguntas del módulo FIES, en contraparte, el 19% respondieron 
    afirmativamente todas las preguntas.
    """)
    
    st.markdown("#### Ilustración 1. Porcentaje de respuestas afirmativas por pregunta en módulo FIES")
    
    # Crear datos para la tabla de respuestas afirmativas
    respuestas_data = {
        "RS": [0, 1, 2, 3, 4, 5, 6, 7, 8],
        "%": ["23%", "14%", "7%", "9%", "7%", "7%", "7%", "9%", "19%"]
    }
    
    # Mostrar como tabla
    st.table(pd.DataFrame(respuestas_data))
    
    # Separador
    st.markdown("---")
    
    # Tercera fila - Equating (2 columnas)
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        Antes de comparar las mediciones obtenidas en dos países o poblaciones diferentes es necesario calibrar las dos 
        escalas sobre la base de un sistema de medición común, al igualar la media y la desviación estándar del conjunto 
        de ítems que son comunes a las dos escalas, a partir de un procedimiento denominado "equating". La equiparación 
        es una forma de estandarización de la métrica basada en la identificación del subconjunto de ítems que pueden 
        considerarse comunes a la FIES global y a la escala específica utilizada para la medición en cada contexto.
        
        Como se observa en la Ilustración 2, la alineación de la escala estimada en Paraguay con los estándares globales 
        de la FIES fue satisfactoria: se identificó un conjunto de al menos seis ítems comunes, es decir, se encontró que 
        los niveles de gravedad asociados a estos seis ítems estaban alineados con los niveles correspondientes en la escala 
        global de referencia, lo cual permite llevar a cabo un procedimiento de igualación sólido.
        """)
    
    with col2:
        # Cargar imagen de Ilustración 2
        try:
            st.image(os.path.join(ruta_imagenes, "Ilustración 2 Equiparación de escala FIES.png"), width=400)
        except:
            st.warning("No se pudo cargar la imagen 'Ilustración 2 Equiparación de escala FIES.png'")
        
        # Cuadro de texto con correlación
        st.info("Correlación entre elementos comunes: 98%")
    
    # Separador
    st.markdown("---")
    
    # Cuarta fila - Probabilidad (2 columnas)
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        En la ilustración 3, tanto los parámetros de severidad de la respuesta y los errores estándar se utilizan para 
        estimar la probabilidad de ser inseguro alimentario en los niveles moderado o grave, y grave (Pmod+grave y Pgrave 
        respectivamente). Se evidencia que la probabilidad aumenta con puntajes brutos más altos, lo que induce que a medida 
        que una persona responde más preguntas afirmativamente, tiene una mayor probabilidad de ser categorizado como 
        inseguro moderado o grave.
        """)
    
    with col2:
        # Datos para la tabla de probabilidades
        prob_data = {
            "Puntaje bruto": [0, 1, 2, 3, 4, 5, 6, 7, 8],
            "Porcentaje de Individuos": ["22,6%", "13,6%", "6,7%", "8,8%", "6,8%", "7,1%", "7,1%", "8,9%", "18,5%"],
            "Probabilidad (mod+sev)": [0.0, 0.018060, 0.072649, 0.230484, 0.544816, 0.828988, 0.952523, 0.987277, 0.995779],
            "Probabilidad (sev)": [0.0, 0.000020, 0.000026, 0.000144, 0.001937, 0.025274, 0.171284, 0.561874, 0.858971]
        }
        
        # Convertir a dataframe y formatear
        prob_df = pd.DataFrame(prob_data)
        
        # Formatear las probabilidades para mostrar solo 6 decimales
        prob_df["Probabilidad (mod+sev)"] = prob_df["Probabilidad (mod+sev)"].apply(lambda x: f"{x:.6f}")
        prob_df["Probabilidad (sev)"] = prob_df["Probabilidad (sev)"].apply(lambda x: f"{x:.6f}")
        
        # Mostrar tabla
        st.table(prob_df)
        
        # Pie de página para la tabla
        st.caption("""
        Pmod+grave = probabilidad de que un individuo con determinado puntaje bruto de ser categorizado como inseguro alimentario moderado-grave. 
        Pgrave = probabilidad de que un individuo con determinado puntaje bruto de ser categorizado como inseguro alimentario grave.
        """)
    
    # Separador
    st.markdown("---")
    
    # Quinta fila - Cita centrada
    st.markdown("""
    <div style="text-align: center; padding: 20px; font-style: italic; background-color: #f0f0f0; border-radius: 5px;">
    "La prevalencia de la inseguridad alimentaria en niveles moderados o graves referencia una falta de acceso continuado 
    a los alimentos, lo cual disminuye la calidad de la dieta, altera los hábitos alimentarios normales y puede tener 
    consecuencias negativas para la nutrición, la salud y el bienestar. Por su parte los hogares o personas que afrontan 
    una inseguridad alimentaria grave es probable que se hayan quedado sin alimentos, experimentado hambre y, en las 
    situaciones más extremas, hayan pasado varios días sin comer, lo cual pone su salud y bienestar en grave riesgo."
    </div>
    """, unsafe_allow_html=True)
    
    # Separador
    st.markdown("---")
    
    # Sexta fila - Prevalencias
    st.markdown("""
    En este sentido, las prevalencias de inseguridad alimentaria en personas estimadas en la población de comedores 
    comunitarios de Cali se describen en la ilustración 4.
    """)
    
    st.markdown("#### Ilustración 4. Prevalencias de inseguridad alimentaria en personas beneficiarias del programa de comedores comunitarios (%)")
    
    # Datos para la tabla de prevalencias
    prevalencias_data = {
        "Tasa de prevalencia (Mod+Sev)": ["46,28%"],
        "Tasa de prevalencia (Sev)": ["22,308%"]
    }
    
    # Mostrar tabla de prevalencias
    st.table(pd.DataFrame(prevalencias_data))
    
    # Párrafo final
    st.markdown("""
    Los resultados muestran que el 46,28% o 46 de cada 100 personas se vieron afectados por inseguridad alimentaria 
    moderada o grave durante los últimos 12 meses. Por su parte el 22,3% de los individuos se vieron afectados por 
    inseguridad alimentaria grave durante los últimos 12 meses.
    """)