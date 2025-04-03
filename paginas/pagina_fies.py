import streamlit as st
import pandas as pd
import os

def mostrar_pagina_fies():
    """
    Muestra el contenido de la pestaña FIES
    """
    # Verificar si existen las carpetas de imágenes
    ruta_imagenes = "imagenes"
    
    # Título principal centrado y vistoso (sin imagen)
    st.markdown("""
    <h1 style="text-align: center; color: #1e88e5; padding: 20px; background-color: #f5f5f5; border-radius: 10px; margin-bottom: 20px;">
    APLICACIÓN DE LA ESCALA DE EXPERIENCIA DE INSEGURIDAD ALIMENTARIA (FIES)
    </h1>
    """, unsafe_allow_html=True)
    
    # Primera fila de contenido (solo con la explicación FIES centrada)
    st.markdown("""
    <div style="text-align: center; font-style: italic; padding: 15px; background-color: #f0f8ff; border-radius: 5px; border-left: 4px solid #1e88e5; margin: 20px 0;">
    "La FIES es una herramienta utilizada para estimar la gravedad de la inseguridad alimentaria de individuos u hogares. 
    Las ocho preguntas del módulo están orientadas a revelar condiciones que cubren un rango de severidad y el protocolo 
    analítico de la FIES hace posible transformar la información cualitativa recopilada (respuestas "sí / no") en 
    medidas cuantitativas de la severidad de la situación de inseguridad alimentaria, lo que permite categorizar a los 
    encuestados en clases de inseguridad alimentaria moderada y grave para posteriormente generar las estimaciones."
    </div>
    """, unsafe_allow_html=True)
    
    # Segunda fila - Parámetros del encuestado (dividida en dos columnas)
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <h3 style="color: #1e88e5; border-bottom: 2px solid #1e88e5; padding-bottom: 8px;">
        Parámetros del encuestado
        </h3>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="background-color: #f9f9f9; padding: 15px; border-radius: 5px; border-left: 3px solid #757575;">
        El puntaje bruto de un encuestado es la cantidad de respuestas afirmativas dadas a las ocho preguntas de la FIES, 
        constituyendo un número entero con un valor entre 0 y 8, representando en sí misma, una medida ordinal e intuitiva 
        de la situación de inseguridad alimentaria. Por lo cual, aquellos encuestados con puntajes brutos más altos serán 
        los que estén experimentando situaciones relacionadas con dificultades en el acceso a los alimentos. En la ilustración 1 
        se observa que el <span style="font-weight: bold; color: #d32f2f;">23%</span> respondieron "No" a las ocho preguntas del módulo FIES, en contraparte, el 
        <span style="font-weight: bold; color: #d32f2f;">19%</span> respondieron afirmativamente todas las preguntas.
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <h4 style="color: #333; text-align: center; background-color: #e3f2fd; padding: 10px; border-radius: 5px;">
        Ilustración 1. Porcentaje de respuestas afirmativas por pregunta en módulo FIES
        </h4>
        """, unsafe_allow_html=True)
        
        # Crear datos para la tabla de respuestas afirmativas
        respuestas_data = {
            "RS": [0, 1, 2, 3, 4, 5, 6, 7, 8],
            "%": ["23%", "14%", "7%", "9%", "7%", "7%", "7%", "9%", "19%"]
        }
        
        # Usar DataFrame de pandas para mostrar la tabla con estilo
        resp_df = pd.DataFrame(respuestas_data)
        st.dataframe(resp_df, use_container_width=True)
    
    # Tercera fila - Equating (2 columnas)
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style="background-color: #f5f5f5; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
        <p style="line-height: 1.6; text-align: justify;">
        Antes de comparar las mediciones obtenidas en dos países o poblaciones diferentes es necesario calibrar las dos 
        escalas sobre la base de un sistema de medición común, al igualar la media y la desviación estándar del conjunto 
        de ítems que son comunes a las dos escalas, a partir de un procedimiento denominado <span style="font-weight: bold; color: #1e88e5;">"equating"</span>. La equiparación 
        es una forma de estandarización de la métrica basada en la identificación del subconjunto de ítems que pueden 
        considerarse comunes a la FIES global y a la escala específica utilizada para la medición en cada contexto.
        </p>
        
        <p style="line-height: 1.6; text-align: justify; margin-top: 15px;">
        Como se observa en la Ilustración 2, se identificó un conjunto de al menos <span style="font-weight: bold; color: #1e88e5;">seis ítems comunes</span>, es decir, se encontró que 
        los niveles de gravedad asociados a estos seis ítems estaban alineados con los niveles correspondientes en la escala 
        global de referencia, lo cual permite llevar a cabo un procedimiento de igualación sólido.
        </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # Contenedor para la imagen
        st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
        
        # Cargar imagen de Ilustración 2
        try:
            st.image(os.path.join(ruta_imagenes, "grafico fies.png"), width=400)
        except:
            st.warning("No se pudo cargar la imagen 'grafico fies.png'")
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Cuadro de texto con correlación
        st.markdown("""
        <div style="margin-top: 20px; background-color: #e8f5e9; padding: 12px; border-radius: 5px; border-left: 4px solid #4caf50; text-align: center;">
            <span style="font-weight: bold; font-size: 16px;">Correlación entre elementos comunes:</span> 
            <span style="font-size: 18px; color: #2e7d32; font-weight: bold;">98%</span>
        </div>
        """, unsafe_allow_html=True)
    
    # Cuarta fila - Probabilidad (2 columnas)
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style="background-color: #ede7f6; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
        <p style="line-height: 1.6; text-align: justify;">
        En la ilustración 3, tanto los parámetros de severidad de la respuesta y los errores estándar se utilizan para 
        estimar la probabilidad de ser inseguro alimentario en los niveles moderado o grave, y grave 
        (<span style="font-weight: bold; color: #673ab7;">Pmod+grave</span> y <span style="font-weight: bold; color: #673ab7;">Pgrave</span> 
        respectivamente). Se evidencia que la probabilidad aumenta con puntajes brutos más altos, lo que induce que a medida 
        que una persona responde más preguntas afirmativamente, tiene una mayor probabilidad de ser categorizado como 
        inseguro moderado o grave.
        </p>
        <ul style="margin-top: 15px; line-height: 1.6; text-align: justify;">
            <li><span style="font-weight: bold; color: #673ab7;">22.6% de la población</span> no respondió afirmativamente a ninguna pregunta (puntuación 0), lo que indica seguridad alimentaria.</li>
            <li><span style="font-weight: bold; color: #673ab7;">29.1% de la población</span> (13.6% + 6.7% + 8.8%) tiene puntuaciones bajas (1-3), indicando vulnerabilidad pero con baja probabilidad de inseguridad alimentaria moderada o severa.</li>
            <li><span style="font-weight: bold; color: #673ab7;">13.9% de la población</span> (6.8% + 7.1%) tiene puntuaciones medias (4-5) con probabilidades intermedias de inseguridad alimentaria moderada.</li>
            <li><span style="font-weight: bold; color: #673ab7;">34.5% de la población</span> (7.1% + 8.9% + 18.5%) tiene puntuaciones altas (6-8), con alta probabilidad de inseguridad alimentaria moderada o severa.</li>
        </ul>
        <p style="margin-top: 15px; line-height: 1.6; text-align: justify;">
        <span style="font-weight: bold;">Especialmente notable:</span>
        </p>
        <ul style="line-height: 1.6; text-align: justify;">
            <li><span style="font-weight: bold; color: #673ab7;">18.5% de la población</span> respondió afirmativamente a las 8 preguntas, con un 85.9% de probabilidad de inseguridad alimentaria severa.</li>
            <li>A partir de la puntuación 5, la probabilidad de inseguridad alimentaria moderada+severa supera el 80%.</li>
            <li>La probabilidad de inseguridad alimentaria severa aumenta drásticamente a partir de la puntuación 6.</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # Datos para la tabla de probabilidades
        prob_data = {
            "Puntaje bruto": [0, 1, 2, 3, 4, 5, 6, 7, 8],
            "Porcentaje de Individuos": ["22,6%", "13,6%", "6,7%", "8,8%", "6,8%", "7,1%", "7,1%", "8,9%", "18,5%"],
            "Probabilidad (mod+sev)": [0.0, 0.018060, 0.072649, 0.230484, 0.544816, 0.828988, 0.952523, 0.987277, 0.995779],
            "Probabilidad (sev)": [0.0, 0.000020, 0.000026, 0.000144, 0.001937, 0.025274, 0.171284, 0.561874, 0.858971]
        }
        
        # Crear DataFrame y mostrar tabla
        prob_df = pd.DataFrame(prob_data)
        
        # Formatear las probabilidades para mostrar 6 decimales
        prob_df["Probabilidad (mod+sev)"] = prob_df["Probabilidad (mod+sev)"].apply(lambda x: f"{x:.6f}")
        prob_df["Probabilidad (sev)"] = prob_df["Probabilidad (sev)"].apply(lambda x: f"{x:.6f}")
        
        # Mostrar tabla usando st.dataframe en lugar de HTML personalizado
        st.dataframe(prob_df, use_container_width=True)
        
        # Pie de página para la tabla
        st.caption("""
        Pmod+grave = probabilidad de que un individuo con determinado puntaje bruto sea categorizado como inseguro alimentario moderado-grave. 
        Pgrave = probabilidad de que un individuo con determinado puntaje bruto sea categorizado como inseguro alimentario grave.
        """)
    
    # Quinta fila - Cita centrada
    st.markdown("---")
    
    st.markdown("""
    <div style="text-align: center; padding: 25px; font-style: italic; background-color: #e0f7fa; border-radius: 10px; box-shadow: 0 3px 6px rgba(0,0,0,0.1); margin: 20px 0; position: relative;">
    <span style="font-size: 40px; position: absolute; top: 10px; left: 15px; color: #00acc1; opacity: 0.3;">"</span>
    <p style="font-size: 16px; line-height: 1.8; color: #00697e; z-index: 10; position: relative; padding: 0 30px;">
    La prevalencia de la inseguridad alimentaria en niveles moderados o graves referencia una falta de acceso continuado 
    a los alimentos, lo cual disminuye la calidad de la dieta, altera los hábitos alimentarios normales y puede tener 
    consecuencias negativas para la nutrición, la salud y el bienestar. Por su parte los hogares o personas que afrontan 
    una inseguridad alimentaria grave es probable que se hayan quedado sin alimentos, experimentado hambre y, en las 
    situaciones más extremas, hayan pasado varios días sin comer, lo cual pone su salud y bienestar en grave riesgo.
    </p>
    <span style="font-size: 40px; position: absolute; bottom: 10px; right: 15px; color: #00acc1; opacity: 0.3;">"</span>
    </div>
    """, unsafe_allow_html=True)
    
    # Sexta fila - Prevalencias
    st.markdown("---")
    
    st.markdown("""
    <div style="background-color: #f9f9f9; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
    <p style="line-height: 1.6; text-align: justify; margin-bottom: 15px;">
    En este sentido, las prevalencias de inseguridad alimentaria en personas estimadas en la población de comedores 
    comunitarios de Cali se describen en la ilustración 4.
    </p>
    
    <h4 style="color: #1565c0; text-align: center; background-color: #e3f2fd; padding: 10px; border-radius: 5px; margin-top: 20px; margin-bottom: 20px;">
    Ilustración 4. Prevalencias de inseguridad alimentaria en personas beneficiarias del programa de comedores comunitarios (%)
    </h4>
    </div>
    """, unsafe_allow_html=True)
    
    # Datos para la tabla de prevalencias
    prevalencias_data = {
        "Tasa de prevalencia (Mod+Sev)": ["46,28%"],
        "Tasa de prevalencia (Sev)": ["22,308%"]
    }
    
    # Crear DataFrame y mostrar tabla
    prevalencias_df = pd.DataFrame(prevalencias_data)
    st.dataframe(prevalencias_df, use_container_width=True)
    
    # Párrafo final con diseño mejorado
    st.markdown("""
    <div style="background-color: #fff8e1; padding: 20px; border-radius: 8px; border-left: 5px solid #ffc107; margin-top: 20px; box-shadow: 0 2px 4px rgba(0,0,0,0.05);">
    <p style="line-height: 1.7; text-align: justify;">
    Los resultados muestran que el <span style="font-weight: bold; color: #d32f2f;">46,28%</span> o 46 de cada 100 personas se vieron afectados por inseguridad alimentaria 
    moderada o grave durante los últimos 12 meses. Por su parte el <span style="font-weight: bold; color: #d32f2f;">22,3%</span> de los individuos se vieron afectados por 
    inseguridad alimentaria grave durante los últimos 12 meses.
    </p>
    </div>
    """, unsafe_allow_html=True)