import streamlit as st
import requests
import time

# ----------------------------------
# Configuration
# ----------------------------------
BLYNK_AUTH = "YOUR_BLYNK_AUTH_TOKEN"  # Replace with your actual token
BASE_URL = f"https://blynk.cloud/external/api"

# Helper functions
def get_virtual_pin(pin):
    """Read data from a virtual pin"""
    try:
        url = f"{BASE_URL}/get?token={BLYNK_AUTH}&{pin}"
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        else:
            return "Error"
    except Exception as e:
        return str(e)

def set_virtual_pin(pin, value):
    """Write data to a virtual pin"""
    try:
        url = f"{BASE_URL}/update?token={BLYNK_AUTH}&{pin}={value}"
        requests.get(url)
    except Exception as e:
        st.error(f"Error sending data: {e}")

# ----------------------------------
# Streamlit UI
# ----------------------------------
st.set_page_config(page_title="IoT Dashboard with Blynk", layout="wide")
st.title("🌐 IoT Dashboard using Blynk (Virtual Pins)")

col1, col2 = st.columns(2)

with col1:
    st.subheader("📊 Sensor Readings")
    refresh = st.button("🔄 Refresh Data")

    temp = get_virtual_pin("V0")
    hum = get_virtual_pin("V1")

    st.metric(label="🌡️ Temperature", value=f"{temp} °C")
    st.metric(label="💧 Humidity", value=f"{hum} %")

with col2:
    st.subheader("💡 Device Control")

    led_state = st.toggle("LED (V2)")
    if led_state:
        set_virtual_pin("V2", 1)
        st.success("LED turned ON")
    else:
        set_virtual_pin("V2", 0)
        st.warning("LED turned OFF")

# Optional: Auto-refresh section
st.markdown("---")
st.subheader("📈 Live Monitor (auto-refresh every 5 sec)")

placeholder = st.empty()
for _ in range(10):  # updates 10 times, then stops
    with placeholder.container():
        temp = get_virtual_pin("V0")
        hum = get_virtual_pin("V1")
        st.metric(label="🌡️ Temperature", value=f"{temp} °C")
        st.metric(label="💧 Humidity", value=f"{hum} %")
    time.sleep(5)
