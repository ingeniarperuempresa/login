import streamlit as st
import pandas as pd

# Configuración de la página
st.set_page_config(
    page_title="Registro desde Google Sheets",
    page_icon="📊",
    layout="wide",
)

# ID del Google Sheet
gsheet_id = '1z27zAFC-b16WC4s3EF9N9vN7Uf2dM-bkO_l4N7kUCJQ'
sheet_id = '0'  # Asumiendo que quieres la primera hoja

# URL para leer los datos en formato CSV
url = f'https://docs.google.com/spreadsheets/d/{gsheet_id}/export?format=csv&gid={sheet_id}'

# Leer los datos del Google Sheet
df = pd.read_csv(url)

# Limpiar la columna de celular: eliminar comas y convertir a string
df['celular'] = df['celular'].astype(str).str.replace(',', '').str.strip()
df['contraseña'] = df['contraseña'].astype(str).str.strip()  # Limpiar la columna de contraseña también

# Función para verificar las credenciales
def verify_login(celular, contraseña):

    
    # Limpiar el celular ingresado
    celular_limpio = celular.replace(',', '').strip()
    
    user_data = df[(df['celular'] == celular_limpio) & (df['contraseña'] == contraseña)]
    
    return not user_data.empty

# Barra lateral para el inicio de sesión
with st.sidebar:
    st.header("Inicio de Sesión")
    celular_input = st.text_input("Número de Celular:")
    contraseña_input = st.text_input("Contraseña:", type="password")
    
    if st.button("Iniciar Sesión"):
        if verify_login(celular_input, contraseña_input):
            st.session_state.logged_in = True
            st.success("¡Inicio de sesión exitoso!")
        else:
            st.error("Número de celular o contraseña incorrectos.")

# Verificar si el usuario está logueado
if st.session_state.get("logged_in"):
    # Mensaje de éxito y no mostrar datos
    st.success("¡Inicio de sesión exitoso!")
else:
    st.warning("Por favor, inicia sesión para ver los datos.")
