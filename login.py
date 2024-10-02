import streamlit as st
import pandas as pd
import google.generativeai as gen_ai

# Configuración de la página
st.set_page_config(
    page_title="Registro de IngenIAr",
    page_icon="📊",
    layout="wide",
)

# Configurar la API de Google
GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
gen_ai.configure(api_key=GOOGLE_API_KEY)
generation_config = {
    "temperature": 0.7,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
}

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

# Función para verificar las credenciales y obtener el nombre y otros datos
def verify_login(celular, contraseña):
    celular_limpio = celular.replace(',', '').strip()
    user_data = df[(df['celular'] == celular_limpio) & (df['contraseña'] == contraseña)]
    
    if not user_data.empty:
        return user_data.iloc[0]['nombre'], user_data.iloc[0]['sueños'], user_data.iloc[0]['time'], user_data.iloc[0]['hechos'], user_data.iloc[0].get('metas', None), user_data.iloc[0].get('nivel', None)
    return None, None, None, None, None, None

# Barra lateral para el inicio de sesión
with st.sidebar:
    st.image("logo2.png", width=70)  # Asegúrate de que la imagen esté en la ruta correcta
    st.header("Inicio de Sesión")
    celular_input = st.text_input("Número de Celular:")
    contraseña_input = st.text_input("Contraseña:", type="password")
    
    if st.button("Iniciar Sesión"):
        nombre, sueños, time, hechos, metas, nivel = verify_login(celular_input, contraseña_input)
        if nombre:
            st.session_state.logged_in = True
            st.session_state.nombre = nombre
            st.session_state.sueños = sueños
            st.session_state.time = time
            st.session_state.hechos = hechos
            st.session_state.metas = metas
            st.session_state.nivel = nivel
            st.success("¡Inicio de sesión exitoso!")
        else:
            st.error("Número de celular o contraseña incorrectos.")

# Mostrar el mensaje personalizado solo si el usuario está logueado
if st.session_state.get("logged_in"):
    st.write(f"Hola {st.session_state.nombre}, actualmente estás en el nivel {st.session_state.nivel}.")
    st.write("¡Listo para seguir cumpliendo nuevos retos!")

    # Mostrar las metas del usuario
    metas = st.session_state.get("metas")
    if metas:
        if isinstance(metas, str):
            st.write("Tus metas son:")
            for meta in metas.split(','):
                st.write(f"- {meta.strip()}")
        else:
            st.write("No se pudo procesar las metas.")
    else:
        prompt = f"Genera una lista de 7 objetivos que deba cumplir si o si para lograr {st.session_state.sueños}."
        try:
            model = gen_ai.GenerativeModel(
                model_name="gemini-1.5-flash",
                generation_config=generation_config,
                system_instruction="Eres un planificador de metas para que las personas cumplan sus objetivos."
            )
            gemini_response = model.generate(prompt)
            st.text_area("Texto generado:", value=gemini_response.text, height=200, key="generated_content", help="Puedes copiar el texto generado seleccionándolo.", disabled=False)
        except Exception as e:
            st.error(f"Ocurrió un error al generar la respuesta: {e}")

else:
    st.warning("👈 Despliega el panel lateral para iniciar sesión.")
