import json
import os
import gspread
from google.oauth2.service_account import Credentials
import streamlit as st
import pandas as pd
from dotenv import load_dotenv

# Cargar variables de entorno desde .env para desarrollo local
load_dotenv()

# Función para establecer conexión con Google Sheets
def connect_to_gsheets():
    # Intentar obtener credenciales de múltiples fuentes
    
    # 1. Primero intentar desde secretos de Streamlit (para producción)
    if hasattr(st, "secrets") and "gcp_service_account" in st.secrets:
        try:
            # Obtener credenciales directamente como diccionario
            credentials_info = dict(st.secrets["gcp_service_account"])
            
            # Configurar las credenciales sin necesidad de archivo temporal
            scopes = ['https://spreadsheets.google.com/feeds',
                     'https://www.googleapis.com/auth/drive']
            
            creds = Credentials.from_service_account_info(credentials_info, scopes=scopes)
            client = gspread.authorize(creds)
            return client
        except Exception as e:
            st.error(f"Error al usar credenciales de Streamlit Secrets: {e}")
    
    # 2. Si no se encontraron en secretos, intentar desde variables de entorno
    credentials_json = os.getenv("GOOGLE_CREDENTIALS")
    
    if not credentials_json:
        st.error("No se encontraron las credenciales en las variables de entorno ni en Streamlit Secrets")
        return None
        
    # Convertir el string JSON a diccionario
    try:
        credentials_info = json.loads(credentials_json)
    except json.JSONDecodeError:
        st.error("Error al decodificar las credenciales JSON")
        return None

    # Guardar las credenciales temporalmente en un archivo
    with open('temp_credentials.json', 'w') as f:
        json.dump(credentials_info, f)
    
    # Configurar las credenciales
    scopes = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']
    
    try:
        creds = Credentials.from_service_account_file('temp_credentials.json', scopes=scopes)
        client = gspread.authorize(creds)
        # Eliminar el archivo temporal
        os.remove('temp_credentials.json')
        return client
    except Exception as e:
        st.error(f"Error al conectar con Google Sheets: {e}")
        # Intentar eliminar el archivo temporal si existe
        try:
            os.remove('temp_credentials.json')
        except:
            pass
        return None

# Función para cargar datos
def load_data(sheet_id, sheet_name=0):
    try:
        client = connect_to_gsheets()
        if client:
            # Abrir la hoja por ID
            sheet = client.open_by_key(sheet_id)
            # Obtener la primera hoja o la especificada
            worksheet = sheet.get_worksheet(sheet_name) if isinstance(sheet_name, int) else sheet.worksheet(sheet_name)
            # Obtener todos los datos
            data = worksheet.get_all_records()
            return pd.DataFrame(data)
        else:
            st.error("No se pudo conectar con Google Sheets")
            return None
    except Exception as e:
        st.error(f"Error al cargar los datos: {e}")
        return None