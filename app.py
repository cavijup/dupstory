import streamlit as st

# IMPORTANTE: set_page_config debe ser la primera llamada a funciones de Streamlit
st.set_page_config(
    page_title="DUB Data Visualization",
    page_icon="📊",
    layout="wide"
)

# Ahora podemos importar el resto de módulos
from paginas.pagina_dub import mostrar_pagina_dub
from paginas.pagina_fies import mostrar_pagina_fies
from paginas.pagina_demografia import mostrar_pagina_demografia
from paginas.mapa import mostrar_mapa

# Estilos personalizados para fondo blanco
st.markdown("""
    <style>
    .main {
        background-color: white;
        color: black;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: white;
        border-radius: 4px 4px 0px 0px;
        gap: 1px;
        padding-top: 10px;
        padding-bottom: 10px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #f0f0f0;
        border-bottom: 2px solid #4c9aff;
    }
    </style>
""", unsafe_allow_html=True)

def main():
    st.title("Dashboard de Visualización de Datos DUB")
    
    # Crear pestañas para la navegación con MAPA justo después de DUB
    tab1, tab4, tab2, tab3 = st.tabs(["DUB", "MAPA", "FIES", "DEMOGRAFÍA"])
    
    # Contenido para cada pestaña
    with tab1:
        # Guardar el dataframe en session_state para compartirlo entre pestañas
        df = mostrar_pagina_dub()
        if df is not None:
            st.session_state.df = df
    
    with tab4:
        mostrar_mapa()
        
    with tab2:
        mostrar_pagina_fies()
    
    with tab3:
        mostrar_pagina_demografia()
    
    # Agregar pie de página
    st.markdown("---")
    st.caption("Desarrollado con Streamlit • Datos actualizados desde Google Sheets")