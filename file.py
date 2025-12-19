import streamlit as st
import requests
import pandas as pd

# --------- Config ---------
st.set_page_config(page_title="Pakistan Weather & AQI Dashboard", layout="wide")

st.title("🌤️ Pakistan Weather & Air Quality Dashboard")
st.write("Live weather and air quality data for major Pakistani cities")

# --------- Cities & APIs ---------
cities = ["Karachi", "Lahore", "Islamabad", "Faisalabad", "Peshawar"]
weather_api_key = "YOUR_OPENWEATHERMAP_API_KEY"  # Signup for free API
aqi_base_url = "https://api.waqi.info/feed/{}/?token=YOUR_WAQI_API_KEY"

# --------- Functions ---------
def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city},PK&appid={weather_api_key}&units=metric"
    response = requests.get(url).json()
    temp = response["main"]["temp"]
    humidity = response["main"]["humidity"]
    wind = response["wind"]["speed"]
    return temp, humidity, wind

def get_aqi(city):
    url = aqi_base_url.format(city)
    response = requests.get(url).json()
    if response["status"] == "ok":
        aqi = response["data"]["aqi"]
    else:
        aqi = None
    return aqi

# --------- Sidebar ---------
selected_city = st.sidebar.selectbox("Select a City", cities)

# --------- Fetch Data ---------
weather = get_weather(selected_city)
aqi = get_aqi(selected_city)

# --------- Display Data ---------
st.subheader(f"Weather in {selected_city}")
st.write(f"🌡️ Temperature: {weather[0]}°C")
st.write(f"💧 Humidity: {weather[1]}%")
st.write(f"💨 Wind Speed: {weather[2]} m/s")

st.subheader(f"Air Quality Index (AQI) in {selected_city}")
if aqi:
    st.write(f"🌫️ AQI: {aqi}")
    if aqi <= 50:
        st.success("Good")
    elif aqi <= 100:
        st.info("Moderate")
    elif aqi <= 150:
        st.warning("Unhealthy for Sensitive Groups")
    elif aqi <= 200:
        st.error("Unhealthy")
    elif aqi <= 300:
        st.error("Very Unhealthy")
    else:
        st.error("Hazardous")
else:
    st.write("AQI data not available")

# --------- Table for all cities ---------
st.subheader("📊 Weather & AQI for Major Cities")
data_list = []
for city in cities:
    w = get_weather(city)
    a = get_aqi(city)
    data_list.append({
        "City": city,
        "Temperature (°C)": w[0],
        "Humidity (%)": w[1],
        "Wind Speed (m/s)": w[2],
        "AQI": a if a else "N/A"
    })

df = pd.DataFrame(data_list)
st.dataframe(df)
