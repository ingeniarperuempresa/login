import streamlit as st
import pandas as pd
import time
import gen_ai  # Asegúrate de importar tu módulo de IA

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

# Limpiar las columnas
df['celular'] = df['celular'].astype(str).str.replace(',', '').str.strip()
df['contraseña'] = df['contraseña'].astype(str).str.strip()

# Función para verificar las credenciales y obtener el nombre y sueño
def verify_login(celular, contraseña):
    celular_limpio = celular.replace(',', '').strip()
    user_data = df[(df['celular'] == celular_limpio) & (df['contraseña'] == contraseña)]
    
    if not user_data.empty:
        return user_data.iloc[0]['nombre'], user_data.iloc[0]['sueños'], user_data.iloc[0]['time'], user_data.iloc[0]['hechos']
    return None, None, None, None

# Barra lateral para el inicio de sesión
with st.sidebar:
    st.image("logo2.png", width=70)
    st.header("Inicio de Sesión")
    celular_input = st.text_input("Número de Celular:")
    contraseña_input = st.text_input("Contraseña:", type="password")
    
    if st.button("Iniciar Sesión"):
        nombre, sueños, tiempo, hechos = verify_login(celular_input, contraseña_input)
        if nombre:
            st.session_state.logged_in = True
            st.session_state.nombre = nombre
            st.session_state.sueños = sueños
            st.session_state.tiempo = tiempo
            st.session_state.hechos = hechos
            st.success("¡Inicio de sesión exitoso!")
        else:
            st.error("Número de celular o contraseña incorrectos.")

# Funcionalidad adicional después de iniciar sesión
if st.session_state.get("logged_in"):
    st.write(f"Hola {st.session_state.nombre}, tu sueño es: {st.session_state.sueños}.")

    # Prompt para la IA de Gemini
    prompt = f"""
    Analiza la situación del usuario basado en los siguientes datos:
    - Sueños: {st.session_state.sueños}
    - Tiempo: {st.session_state.tiempo}
    - Hechos: {st.session_state.hechos}

    Por favor, proporciona:
    - Un nivel del 1 al 5 basado en la información anterior.
    - Objetivos que el usuario debe cumplir para avanzar al siguiente nivel.
    """

    if st.button("Analizar con Gemini"):
        try:
            model = gen_ai.GenerativeModel(
                model_name="gemini-1.5-flash",
                generation_config={
                    "temperature": 1,
                    "top_p": 0.95,
                    "top_k": 64,
                    "max_output_tokens": 8192,
                },
                system_instruction="Eres un analista que proporciona evaluación de objetivos y niveles."
            )

            chat_session = model.start_chat(history=[])

            # Barra de progreso
            progress = st.progress(0)
            for i in range(100):
                time.sleep(0.05)  # Simulación de tiempo de espera
                progress.progress(i + 1)

            gemini_response = chat_session.send_message(prompt)

            st.markdown(f"### Respuesta de Gemini:\n{gemini_response.text}")
        except Exception as e:
            st.error(f"Ocurrió un error al analizar la información: {str(e)}")

else:
    st.warning("👈 Despliega el panel lateral para iniciar sesión.")

