import streamlit as st
import google.generativeai as gen_ai

# Configuración de la página
st.set_page_config(page_title="Registro de IngenIAr", page_icon="📊", layout="wide")

# Configurar la API de Google
GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
gen_ai.configure(api_key=GOOGLE_API_KEY)

# Configuración de generación
generation_config = {
    "temperature": 0.7,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
}

# Función para verificar las credenciales
def verify_login(celular, contraseña):
    # Aquí va la lógica para verificar el usuario (como lo tenías)
    # Retorna el nombre, sueños, hechos, metas, nivel
    return nombre, sueños, hechos, metas, nivel

# Lógica del inicio de sesión
with st.sidebar:
    st.header("Inicio de Sesión")
    celular_input = st.text_input("Número de Celular:")
    contraseña_input = st.text_input("Contraseña:", type="password")

    if st.button("Iniciar Sesión"):
        nombre, sueños, hechos, metas, nivel = verify_login(celular_input, contraseña_input)
        if nombre:
            st.session_state.logged_in = True
            st.session_state.nombre = nombre
            st.session_state.sueños = sueños
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
        prompt = f"Genera una lista de 7 objetivos que deba cumplir si o si para lograr {st.session_state.sueños}"
        try:
            model = gen_ai.GenerativeModel(
                model_name="gemini-1.5-flash",
                generation_config=generation_config,
                system_instruction="Eres un planificador de metas."
            )
            chat_session = model.start_chat(history=[])
            gemini_response = chat_session.send_message(prompt)
            st.write("Aquí tienes algunos objetivos generados:")
            st.text_area("Objetivos generados:", value=gemini_response.text, height=200, disabled=False)
        except Exception as e:
            st.error(f"Ocurrió un error al generar los objetivos: {str(e)}")
else:
    st.warning("👈 Despliega el panel lateral para iniciar sesión.")
