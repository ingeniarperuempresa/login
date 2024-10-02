import streamlit as st
import pandas as pd
import plotly.express as px 

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

# Mostrar los datos en la aplicación
st.write("Datos de Google Sheets:")
st.dataframe(df, use_container_width=True)

# Graficar alguna de las columnas (ejemplo: contar las ocurrencias de "sueños")
if 'sueños' in df.columns:
    sueño_counts = df['sueños'].value_counts().reset_index()
    sueño_counts.columns = ['sueños', 'count']
    
    fig = px.bar(sueño_counts, x='sueños', y='count', title='Frecuencia de Sueños')
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("La columna 'sueños' no se encuentra en los datos.")
