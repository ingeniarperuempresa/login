import streamlit as st
import pandas as pd

# Configuración de la página
st.set_page_config(
    page_title="Registro de IngenIAr",
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

# Función para verificar las credenciales y obtener el nombre y sueño
def verify_login(celular, contraseña):
    celular_limpio = celular.replace(',', '').strip()
    user_data = df[(df['celular'] == celular_limpio) & (df['contraseña'] == contraseña)]
    
    if not user_data.empty:
        return user_data.iloc[0]['nombre'], user_data.iloc[0]['sueños']  # Retorna nombre y sueño
    return None, None

# Barra lateral para el inicio de sesión
with st.sidebar:
    st.header("Inicio de Sesión")
    celular_input = st.text_input("Número de Celular:")
    contraseña_input = st.text_input("Contraseña:", type="password")
    
    if st.button("Iniciar Sesión"):
        nombre, sueños = verify_login(celular_input, contraseña_input)
        if nombre:
            st.session_state.logged_in = True
            st.session_state.nombre = nombre  # Guardar el nombre en la sesión
            st.session_state.sueños = sueños  # Guardar el sueño en la sesión
            st.success("¡Inicio de sesión exitoso!")
        else:
            st.error("Número de celular o contraseña incorrectos.")

# Mostrar el mensaje personalizado solo si el usuario está logueado
if st.session_state.get("logged_in"):
    st.write(f"Hola {st.session_state.nombre}, tu sueño es: {st.session_state.sueños}.")
else:
    st.warning("👈 Despliega el panel lateral para iniciar sesión.")
    st.image("logo.png", width=50 height=50)  # Cambia el tamaño de la imagen aquí
