
import streamlit as st
import pandas as pd
import requests

BACKEND_URL = "https://nifty-coach-backend.onrender.com"

st.set_page_config(page_title="Nifty Trade Coach", layout="wide")
st.markdown("<h1 style='text-align: center;'>📊 Nifty Trade Coach Dashboard</h1>", unsafe_allow_html=True)

# Load trades
@st.cache_data(ttl=300)
def load_trades():
    try:
        r = requests.get(f"{BACKEND_URL}/get_trades")
        if r.status_code == 200:
            return pd.DataFrame(r.json())
        return pd.DataFrame()
    except Exception as e:
        st.error(f"API Error: {e}")
        return pd.DataFrame()

df = load_trades()

if df.empty:
    st.warning("No trades found.")
    st.stop()

# Format & sort
df['timestamp'] = pd.to_datetime(df['timestamp'])
df.sort_values(by="timestamp", ascending=False, inplace=True)

# Sidebar filters
st.sidebar.header("🔍 Filter Trades")
symbol_filter = st.sidebar.multiselect("Symbol", sorted(df["symbol"].unique()))
side_filter = st.sidebar.multiselect("Side", ["BUY", "SELL"])
date_range = st.sidebar.date_input("Date Range", [])

filtered = df.copy()
if symbol_filter:
    filtered = filtered[filtered["symbol"].isin(symbol_filter)]
if side_filter:
    filtered = filtered[filtered["side"].isin(side_filter)]
if len(date_range) == 2:
    start, end = pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])
    filtered = filtered[(filtered["timestamp"] >= start) & (filtered["timestamp"] <= end)]

# KPI row
c1, c2, c3 = st.columns(3)
c1.metric("Total Trades", len(filtered))
c2.metric("Buy Trades", (filtered["side"] == "BUY").sum())
c3.metric("Sell Trades", (filtered["side"] == "SELL").sum())

# Color-coded side column
def highlight_side(val):
    color = "#00cc44" if val == "BUY" else "#ff4d4d"
    return f"color: {color}; font-weight: bold"

# Render table
styled = filtered.style.format({
    "qty": "{:.0f}",
    "price": "₹{:.2f}",
    "timestamp": lambda x: x.strftime("%Y-%m-%d %H:%M")
}).applymap(highlight_side, subset=["side"])

st.markdown("### 📅 Your Trades")
st.dataframe(styled, use_container_width=True)
