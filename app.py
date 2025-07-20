
import streamlit as st
import pandas as pd
import requests
from datetime import datetime

BACKEND_URL = "https://nifty-coach-backend.onrender.com"

st.set_page_config(page_title="Nifty Trade Coach", layout="wide")
st.title("📈 Nifty Trade Coach")

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

# Format and enrich
df['timestamp'] = pd.to_datetime(df['timestamp'])
df['date'] = df['timestamp'].dt.date
df['symbol_readable'] = df['symbol'].fillna("").apply(
    lambda x: x.replace("NIFTY", "NIFTY ").replace("CE", " CE").replace("PE", " PE")
              .replace("BANKNIFTY", "BANKNIFTY ") if isinstance(x, str) else x
)
df.sort_values(by="timestamp", inplace=True)

# PnL estimation (naive matching of Buy → Sell per symbol)
pnl_map = {}
running_positions = {}

for idx, row in df.iterrows():
    sym = row['symbol']
    qty = row['qty']
    price = row['price']
    side = row['side']
    ts = row['timestamp']

    if sym not in running_positions:
        running_positions[sym] = []

    if side == "BUY":
        running_positions[sym].append((qty, price, ts))
        df.at[idx, 'pnl'] = 0.0
    elif side == "SELL" and running_positions[sym]:
        buy_qty, buy_price, buy_ts = running_positions[sym].pop(0)
        pnl = (price - buy_price) * buy_qty
        df.at[idx, 'pnl'] = pnl
    else:
        df.at[idx, 'pnl'] = 0.0

# Group by date and display
st.markdown("### 🧾 Daily Trades Breakdown")

for date in df['date'].unique()[::-1]:
    day_df = df[df['date'] == date].copy()
    day_pnl = day_df['pnl'].sum()
    c1, c2 = st.columns([3, 1])
    c1.markdown(f"#### 📅 {date.strftime('%A, %d %B %Y')}")
    c2.metric("Day P/L", f"₹{day_pnl:.2f}", delta=None, delta_color="inverse")

    display_df = day_df[['timestamp', 'symbol_readable', 'side', 'qty', 'price', 'pnl']].copy()
    display_df.rename(columns={
        'timestamp': 'Time',
        'symbol_readable': 'Symbol',
        'side': 'Side',
        'qty': 'Qty',
        'price': 'Price',
        'pnl': 'P&L'
    }, inplace=True)

    display_df['Time'] = display_df['Time'].dt.strftime('%H:%M:%S')
    st.dataframe(display_df.style.format({
        "Price": "₹{:.2f}",
        "P&L": "₹{:.2f}"
    }).applymap(lambda v: "color: green;" if isinstance(v, (int, float)) and v > 0 else 
                             ("color: red;" if isinstance(v, (int, float)) and v < 0 else ""), subset=["P&L"]),
    use_container_width=True)
    st.markdown("---")
