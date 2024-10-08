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

# Configuración de generación
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
df['celular'] = df['celular'].astype(str).str.replace(',', '').str.strip().str.replace('.0', '')  # Convertir a string y eliminar ".0"
df['contraseña'] = df['contraseña'].astype(str).str.replace(',', '').str.strip().str.replace('.0', '')  # Limpiar la contraseña

# Función para verificar las credenciales y obtener los datos del usuario
def verify_login(celular, contraseña):
    celular_limpio = celular.replace(',', '').strip()
    user_data = df[(df['celular'] == celular_limpio) & (df['contraseña'] == contraseña)]
    
    # Depuración: mostrar los datos que se están buscando
    st.write("Buscando datos para:", celular_limpio, "con contraseña:", contraseña)
    st.write("Datos del DataFrame:", df)

    if not user_data.empty:
        st.write("Usuario encontrado:", user_data)
        return (
            user_data.iloc[0]['nombre'],
            celular_limpio,
            user_data.iloc[0]['contraseña'],
            user_data.iloc[0]['sueños'],
            user_data.iloc[0]['time'],
            user_data.iloc[0]['hechos'],
            user_data.iloc[0].get('metas', None),
            user_data.iloc[0].get('nivel', None),
            user_data.iloc[0].get('promt', None),
            user_data.iloc[0].get('promt2', None),
            user_data.iloc[0].get('estado', None)
        )
    return (None,) * 11  # Devuelve 11 valores None si no se encuentra el usuario

# Barra lateral para el inicio de sesión
with st.sidebar:
    st.image("logo2.png", width=70)  # Asegúrate de que la imagen esté en la ruta correcta
    st.header("Inicio de Sesión")
    celular_input = st.text_input("Número de Celular:")
    contraseña_input = st.text_input("Contraseña:", type="password")
    
    if st.button("Iniciar Sesión"):
        nombre, celular, contraseña, sueños, time, hechos, metas, nivel, promt, promt2, estado = verify_login(celular_input, contraseña_input)
        if nombre:
            st.session_state.logged_in = True
            st.session_state.nombre = nombre
            st.session_state.sueños = sueños
            st.session_state.time = time
            st.session_state.hechos = hechos
            st.session_state.metas = metas
            st.session_state.nivel = nivel
            st.session_state.promt = promt
            st.session_state.promt2 = promt2
            st.session_state.estado = estado 
            st.success("¡Inicio de sesión exitoso!")
        else:
            st.error("Número de celular o contraseña incorrectos.")

# Mostrar el mensaje personalizado solo si el usuario está logueado
if st.session_state.get("logged_in"):
    st.write(f"Hola {st.session_state.nombre}, actualmente estás en el nivel {st.session_state.nivel}.")
    st.write("¡Listo para seguir cumpliendo nuevos retos!")

    # Mostrar las metas del usuario
    metas = st.session_state.get("metas")
    
    if metas is not None and isinstance(metas, str) and metas.strip() != "":
        st.write("Tus metas son:")
        for meta in metas.split(','):  # Asumiendo que las metas están separadas por comas
            st.write(f"- {meta.strip()}")
    else:
        # Generar objetivos si no hay metas
        prompt = f"{st.session_state.sueños} en el tiempo {st.session_state.time} y hasta ahora he hecho {st.session_state.hechos}."
        
        # Crear el modelo
        model = gen_ai.GenerativeModel(
            model_name="gemini-1.5-flash",
            generation_config=generation_config,
            system_instruction="eres un asistente de ingeniar, una empresa que se encarga de ayudar a las personas a cumplir sus metas, mira vas a establecer objetivos de acuerdo a lo que quieran lograr, en el tiempo que quieran lograr esas metas y lo que ya van haciendo y los vas a colocar en un nivel del 1 al 5, depende en donde se encuentren avanzando y vas a colocar de 5 objetivos y harás como si fuera un juego, que necesita cumplir para pasar al siguiente nivel, le darás del nivel 1 para pasar al nivel 2 que objetivos cumplir, después del nivel 2 al 3 que objetivos debe cumplir, así hasta llegar hasta el 5, pero que no sean cosas generales, sino que sean cosas específicas que lo guíen."
        )
        chat_session = model.start_chat(history=[])

        # Asegúrate de utilizar el método correcto para generar la respuesta
        gemini_response = chat_session.send_message(prompt)

        # Mostrar el contenido generado como texto
        st.markdown(f"**Objetivos Generados:**\n\n{gemini_response.text}")

else:
    st.warning("👈 Despliega el panel lateral para iniciar sesión.")
