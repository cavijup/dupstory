import streamlit as st

# IMPORTANTE: set_page_config debe ser la primera llamada a funciones de Streamlit
st.set_page_config(
    page_title="DUB Data Visualization",
    page_icon="📊",
    layout="wide"
)

# Ahora podemos importar el resto de módulos
from paginas.pagina_infordub import mostrar_pagina_infordub
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

# Función principal de la aplicación
def main():
    st.title("Dashboard de Visualización de Datos DUB")
    
    # Crear pestañas para la navegación (ahora con 5 pestañas)
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["INFORDUB", "DUB", "MAPA", "FIES", "DEMOGRAFÍA"])
    
    # Contenido para cada pestaña
    with tab1:
        # La nueva pestaña INFORDUB
        df = mostrar_pagina_infordub()
        if df is not None and 'df' not in st.session_state:
            st.session_state.df = df
    
    with tab2:
        # Esta pestaña ahora solo mostrará el contenido demográfico
        mostrar_pagina_dub()
    
    with tab3:
        # Mapa
        mostrar_mapa()
    
    with tab4:
        # FIES
        mostrar_pagina_fies()
    
    with tab5:
        # DEMOGRAFÍA
        mostrar_pagina_demografia()
    
    # Agregar pie de página
    st.markdown("---")
    st.caption("Desarrollado con Streamlit • Datos actualizados desde Google Sheets")

if __name__ == "__main__":
    main()