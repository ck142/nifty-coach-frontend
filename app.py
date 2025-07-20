
import streamlit as st
import requests

st.set_page_config(page_title="Nifty Trade Coach", layout="wide")
st.title("📈 Nifty Trade Coach Dashboard")

try:
    response = requests.get("https://nifty-backend.onrender.com/ping")
    if response.ok:
        st.success("✅ Backend is alive!")
    else:
        st.error("⚠️ Failed to connect to backend.")
except Exception as e:
    st.error(f"Connection error: {e}")
