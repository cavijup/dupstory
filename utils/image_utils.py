import streamlit as st
import requests
from PIL import Image
from io import BytesIO

def mostrar_imagen_drive(file_id, width=None):
    """
    Muestra una imagen de Google Drive en Streamlit usando métodos más confiables.
    
    Args:
        file_id: ID del archivo en Google Drive
        width: Ancho opcional para mostrar la imagen
    """
    # Método más seguro: usar iframe para incrustar la vista previa de Google Drive
    html_code = f"""
    <div style="display: flex; justify-content: center; margin-bottom: 20px;">
        <iframe src="https://drive.google.com/file/d/{file_id}/preview" 
            width="{width if width else 500}" 
            height="{int((width if width else 500) * 0.75)}" 
            frameborder="0" scrolling="no">
        </iframe>
    </div>
    """
    st.markdown(html_code, unsafe_allow_html=True)
    
    # Nota: si prefieres ver la imagen directamente en lugar de a través de un iframe,
    # descomenta el código a continuación (pero es menos confiable)
    
    """
    try:
        # Intentar cargar directamente usando la API de exportación de Google Drive
        image_url = f"https://drive.google.com/uc?export=view&id={file_id}"
        
        # Descargar la imagen y mostrarla como bytes
        response = requests.get(image_url)
        if response.status_code == 200:
            img = Image.open(BytesIO(response.content))
            st.image(img, width=width)
        else:
            # Si falla, usar el iframe como respaldo
            st.warning("No se pudo cargar la imagen directamente, mostrando vista previa alternativa.")
            html_code = f'''
            <div style="display: flex; justify-content: center;">
                <iframe src="https://drive.google.com/file/d/{file_id}/preview" 
                    width="{width if width else 500}" 
                    height="{int((width if width else 500) * 0.75)}" 
                    frameborder="0">
                </iframe>
            </div>
            '''
            st.markdown(html_code, unsafe_allow_html=True)
    
    except Exception as e:
        st.error(f"Error al mostrar la imagen: {e}")
        # Usar el iframe como último recurso
        html_code = f'''
        <div style="display: flex; justify-content: center;">
            <iframe src="https://drive.google.com/file/d/{file_id}/preview" 
                width="{width if width else 500}" 
                height="{int((width if width else 500) * 0.75)}" 
                frameborder="0">
            </iframe>
        </div>
        '''
        st.markdown(html_code, unsafe_allow_html=True)
    """