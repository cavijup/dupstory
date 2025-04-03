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
    
    # Separador
    st.markdown("---")
    
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
        
        # Convertir a DataFrame
        resp_df = pd.DataFrame(respuestas_data)
        
        # Crear HTML para una tabla más atractiva
        html_table = """
        <table style="width:100%; border-collapse: collapse; text-align:center; margin-top:20px;">
            <thead>
                <tr style="background-color:#1e88e5; color:white; font-weight:bold;">
                    <th style="padding:10px; border:1px solid #ddd;">RS</th>
                    <th style="padding:10px; border:1px solid #ddd;">%</th>
                </tr>
            </thead>
            <tbody>
        """
        
        # Alternar colores para las filas
        for i in range(len(resp_df)):
            bg_color = "#f2f2f2" if i % 2 == 0 else "white"
            html_table += f"""
                <tr style="background-color:{bg_color};">
                    <td style="padding:8px; border:1px solid #ddd;">{resp_df.iloc[i,0]}</td>
                    <td style="padding:8px; border:1px solid #ddd; font-weight:bold;">{resp_df.iloc[i,1]}</td>
                </tr>
            """
        
        html_table += """
            </tbody>
        </table>
        """
        
        st.markdown(html_table, unsafe_allow_html=True)
    
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
        
        Como se observa en la Ilustración 2, se identificó un conjunto de al menos seis ítems comunes, es decir, se encontró que 
        los niveles de gravedad asociados a estos seis ítems estaban alineados con los niveles correspondientes en la escala 
        global de referencia, lo cual permite llevar a cabo un procedimiento de igualación sólido.
        """)
    
    with col2:
        # Contenedor para la imagen con sombra
        st.markdown("""
        <div style="background-color: white; padding: 15px; border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); text-align: center;">
        """, unsafe_allow_html=True)
        
        # Cargar imagen de Ilustración 2
        try:
            st.image(os.path.join(ruta_imagenes, "grafico fies.png"), width=400)
        except:
            st.warning("No se pudo cargar la imagen 'grafico fies.png'")
        
        # Cerrar div contenedor
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Cuadro de texto con correlación
        st.markdown("""
        <div style="margin-top: 20px; background-color: #e8f5e9; padding: 12px; border-radius: 5px; border-left: 4px solid #4caf50; text-align: center;">
            <span style="font-weight: bold; font-size: 16px;">Correlación entre elementos comunes:</span> 
            <span style="font-size: 18px; color: #2e7d32; font-weight: bold;">98%</span>
        </div>
        """, unsafe_allow_html=True)
    
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
        
        # Crear HTML para una tabla más atractiva
        html_table = """
        <div style="background-color: white; padding: 15px; border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.1);">
        <table style="width:100%; border-collapse: collapse; text-align:center; margin-top:10px; font-size:14px;">
            <thead>
                <tr style="background-color:#673ab7; color:white;">
                    <th style="padding:8px; border:1px solid #ddd;">Puntaje bruto</th>
                    <th style="padding:8px; border:1px solid #ddd;">% Individuos</th>
                    <th style="padding:8px; border:1px solid #ddd;">P(mod+sev)</th>
                    <th style="padding:8px; border:1px solid #ddd;">P(sev)</th>
                </tr>
            </thead>
            <tbody>
        """
        
        # Generar filas con colores alternados
        for i in range(len(prob_data["Puntaje bruto"])):
            bg_color = "#f3e5f5" if i % 2 == 0 else "white"
            # Aplicar colores más intensos según aumenta la probabilidad para mod+sev
            mod_sev_val = prob_data["Probabilidad (mod+sev)"][i]
            mod_sev_color = "#ffffff"
            if mod_sev_val > 0.8:
                mod_sev_color = "#c5cae9"
            elif mod_sev_val > 0.5:
                mod_sev_color = "#e8eaf6"
                
            # Aplicar colores más intensos según aumenta la probabilidad para sev
            sev_val = prob_data["Probabilidad (sev)"][i]
            sev_color = "#ffffff"
            if sev_val > 0.5:
                sev_color = "#ffcdd2"
            elif sev_val > 0.1:
                sev_color = "#ffebee"
            
            html_table += f"""
                <tr style="background-color:{bg_color};">
                    <td style="padding:8px; border:1px solid #ddd;">{prob_data["Puntaje bruto"][i]}</td>
                    <td style="padding:8px; border:1px solid #ddd;">{prob_data["Porcentaje de Individuos"][i]}</td>
                    <td style="padding:8px; border:1px solid #ddd; background-color:{mod_sev_color};">{prob_data["Probabilidad (mod+sev)"][i]:.6f}</td>
                    <td style="padding:8px; border:1px solid #ddd; background-color:{sev_color};">{prob_data["Probabilidad (sev)"][i]:.6f}</td>
                </tr>
            """
        
        html_table += """
            </tbody>
        </table>
        """
        
        # Pie de página para la tabla
        html_table += """
        <div style="margin-top: 10px; font-size: 13px; color: #555; font-style: italic; padding: 8px; background-color: #f9f9f9; border-radius: 4px;">
            <p><strong>Pmod+grave</strong> = probabilidad de que un individuo con determinado puntaje bruto sea categorizado como inseguro alimentario moderado-grave.</p> 
            <p><strong>Pgrave</strong> = probabilidad de que un individuo con determinado puntaje bruto sea categorizado como inseguro alimentario grave.</p>
        </div>
        </div>
        """
        
        st.markdown(html_table, unsafe_allow_html=True)
    
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