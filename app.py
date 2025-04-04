import streamlit as st
import requests
from datetime import datetime
import folium
from streamlit_folium import folium_static
import numpy as np

st.markdown("""# Pide tu taxi al mejor precio
            \n## LLAME YA!""")


with st.sidebar:
    st.header("🚕 Configura tu viaje")

    # Selector de fecha y hora
    col1, col2 = st.columns(2)
    with col1:
        pickup_date = st.date_input('Fecha', datetime.now().date())
    with col2:
        pickup_time = st.time_input('Hora', datetime.now().time())
    pickup_datetime = f"{pickup_date} {pickup_time}"

    # Pasajeros
    passengers = st.slider('👥 Pasajeros', 1, 8, 1)
    st.markdown("---")
    st.markdown("📍 **Selecciona ubicaciones en el mapa**")

# Mapa interactivo
st.header("🗺 Selecciona pickup y dropoff en el mapa")


# Mapa centrado en NYC
m = folium.Map(location=[40.7128, -74.0060], zoom_start=12)

# Mostrar mapa
folium_static(m, width=800, height=400)

# Coordenadas por defecto (Times Square a JFK, pq? no sé, se me ocurrio)
pickup_lat, pickup_lon = 40.7580, -73.9855
dropoff_lat, dropoff_lon = 40.6413, -73.7781

# Columnas para mostrar coordenadas
col1, col2 = st.columns(2)
with col1:
    st.subheader("Pickup")
    pickup_lat = st.number_input("Latitud Pickup", value=pickup_lat, key="pickup_lat")
    pickup_lon = st.number_input("Longitud Pickup", value=pickup_lon, key="pickup_lon")

with col2:
    st.subheader("Dropoff")
    dropoff_lat = st.number_input("Latitud Dropoff", value=dropoff_lat, key="dropoff_lat")
    dropoff_lon = st.number_input("Longitud Dropoff", value=dropoff_lon, key="dropoff_lon")


# Entradas básicas
pickup_date = st.date_input('Pickup date', datetime.now())
pickup_time = st.time_input('Pickup time', datetime.now().time())
pickup_datetime = f"{pickup_date} {pickup_time}"

pickup_lon = st.number_input('Pickup longitude', value=-73.98)
pickup_lat = st.number_input('Pickup latitude', value=40.76)
dropoff_lon = st.number_input('Dropoff longitude', value=-73.78)
dropoff_lat = st.number_input('Dropoff latitude', value=40.64)
passengers = st.number_input('Passengers', min_value=1, max_value=8, value=1)

# Botón de predicción
if st.button('Predice tu tarifa (y tu futuro bby)'):
    # Parámetros para la API
    params = {
        "pickup_datetime": pickup_datetime,
        "pickup_longitude": pickup_lon,
        "pickup_latitude": pickup_lat,
        "dropoff_longitude": dropoff_lon,
        "dropoff_latitude": dropoff_lat,
        "passenger_count": passengers,
    }

    try:
            response = requests.get('https://nico-pardo-681692201179.europe-west1.run.app/predict', params=params).json()
            fare = response['fare']

    # Mostrar resultado con estilo
            st.balloons()
            st.markdown(f"""
            <div class="result-box">
                <h2 class="big-font">Tarifa estimada:</h2>
                <h1>${fare:.2f} USD</h1>
                <p>Distancia: {np.random.uniform(3.5, 15.0):.1f} km</p>
                <p>Tiempo estimado: {np.random.randint(15, 45)} minutos</p>
            </div>
            """, unsafe_allow_html=True)

    except Exception as e:
            st.error(f"No pude predecir el precio, perdón : {e}")




    # Llamada a la API
    #response = requests.get('https://nico-pardo-681692201179.europe-west1.run.app', params=params).json()

    # Mostrar resultado
    st.success(f"MIRA ESE PRECIO PAPÁ (muy caro, busca otro lugar): ${response['fare']:.2f}")
