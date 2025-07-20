
import streamlit as st
import pandas as pd
import requests

BACKEND_URL = "https://nifty-coach-backend.onrender.com"

st.set_page_config(page_title="Nifty Trade Coach", layout="wide")
st.title("📊 Nifty Trade Coach Dashboard")

# Load trades from backend
@st.cache_data(ttl=300)
def load_trades():
    try:
        resp = requests.get(f"{BACKEND_URL}/get_trades", timeout=30)
        if resp.status_code == 200:
            return pd.DataFrame(resp.json())
        else:
            st.error(f"Failed to fetch trades: {resp.status_code}")
            return pd.DataFrame()
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return pd.DataFrame()

df = load_trades()

if df.empty:
    st.warning("No trades found.")
else:
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df.sort_values("timestamp", ascending=False, inplace=True)

    with st.expander("📅 Filter by Date"):
        date_range = st.date_input("Select date range", [])
        if len(date_range) == 2:
            start, end = pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])
            df = df[(df['timestamp'] >= start) & (df['timestamp'] <= end)]

    with st.expander("🔍 Filter by Symbol / Side"):
        symbols = st.multiselect("Symbols", options=sorted(df['symbol'].unique().tolist()))
        sides = st.multiselect("Side", options=["BUY", "SELL"])
        if symbols:
            df = df[df['symbol'].isin(symbols)]
        if sides:
            df = df[df['side'].isin(sides)]

    st.markdown(f"### Showing {len(df)} trades")
    st.dataframe(df, use_container_width=True)
