import streamlit as st
import pandas as pd
import pytz
from datetime import datetime
import os
import yfinance as yf
import mplfinance as mpf

# ----- Page Config -----
st.set_page_config(page_title="Trade Reporter - Annotation", layout="wide")
st.title("✍️ Trade Reporter - Étape 2 : Annotation des trades")

# ----- Load uploaded trades -----
try:
    df = pd.read_csv("data/temp_trades.csv")
except FileNotFoundError:
    st.error("Aucun fichier trouvé. Retourne à l'étape 1 pour uploader ton fichier.")
    st.stop()

# ----- Sidebar: Timezone and Capital -----
st.sidebar.header("🕒 Paramètres de fuseau horaire")
timezone = st.sidebar.selectbox("Sélectionne ton fuseau horaire :", pytz.all_timezones, index=pytz.all_timezones.index("Europe/Paris"))
initial_capital = st.sidebar.number_input("💶 Capital initial (€)", min_value=1.0, value=1000.0)

if 'timezone' not in st.session_state or st.session_state.timezone != timezone:
    st.session_state.timezone = timezone

# ----- Session Detection Function -----
def get_session_from_time(trade_time, user_timezone):
    local_tz = pytz.timezone(user_timezone)
    sessions = {
        "Asia": {"start": "00:00", "end": "08:00"},
        "London": {"start": "08:00", "end": "13:00"},
        "New York": {"start": "13:00", "end": "22:00"},
        "After Hours": {"start": "22:00", "end": "00:00"}
    }
    session_times = {}
    for session, times in sessions.items():
        start_time_utc = pytz.utc.localize(datetime.strptime(times["start"], "%H:%M"))
        end_time_utc = pytz.utc.localize(datetime.strptime(times["end"], "%H:%M"))
        start_time_local = start_time_utc.astimezone(local_tz)
        end_time_local = end_time_utc.astimezone(local_tz)
        session_times[session] = {"start": start_time_local, "end": end_time_local}

    for session, times in session_times.items():
        if times["start"].time() <= trade_time.time() < times["end"].time():
            return session
    return "After Hours"

# ----- Chart Plot Function -----
def plot_trade_chart(trade_id, symbol, open_time_str, close_time_str, open_price, close_price):
    yf_symbols = {
        "XAUUSD": "XAUUSD=X",
        "EURUSD": "EURUSD=X",
        "GBPUSD": "GBPUSD=X",
        "NAS100": "^NDX"
    }
    if symbol not in yf_symbols:
        return []

    fmt = "%Y.%m.%d %H:%M:%S"
    open_time = datetime.strptime(open_time_str, fmt)
    close_time = datetime.strptime(close_time_str, fmt)
    start_time = open_time - pd.Timedelta(hours=6)
    end_time = close_time + pd.Timedelta(hours=6)

    plot_paths = []
    for interval in ["15m", "1h"]:
        df = yf.download(yf_symbols[symbol], start=start_time, end=end_time, interval=interval)
        if df.empty:
            continue
        df.index.name = "Date"
        df = df.rename(columns={"Open": "open", "High": "high", "Low": "low", "Close": "close", "Volume": "volume"})
        alines = [
            dict(x=open_time, color="green", linestyle="--", label="Open"),
            dict(x=close_time, color="red", linestyle="--", label="Close")
        ]
        plot_dir = os.path.join("Result", "plots")
        os.makedirs(plot_dir, exist_ok=True)
        filename = f"trade_{trade_id}_{interval}.png"
        full_path = os.path.join(plot_dir, filename)
        mpf.plot(df, type='candle', style='charles', title=f"{symbol} Trade #{trade_id} - {interval}", ylabel='Price', volume=True, alines=alines, savefig=full_path)
        plot_paths.append((interval, full_path))
    return plot_paths

# ----- Trade Annotation Interface -----
edges_dict = {
    "ICT": ["FVG", "OTE", "BOS", "SMT", "Breaker", "Liquidity Sweep", "Judas Swing", "Autre"],
    "SMC": ["CHoCH", "BOS", "FVG", "Order Block", "Liquidity Grab", "Autre"],
    "Wyckoff": ["Spring", "Upthrust", "PSY", "AR", "ST", "LPS", "SOW", "Autre"],
    "Price Action": ["Pin Bar", "Engulfing", "Break & Retest", "Inside Bar", "Autre"],
    "Breakout": ["Breakout Range", "Retest", "Volume Spike", "Autre"],
    "Autre": ["Edge personnalisé"]
}
trade_types = ["Scalping", "Swing", "Position", "Day Trading", "Scalp Intraday", "Autre"]
time_frames = ["1min", "5min", "15min", "1h", "4h", "D", "W"]

st.markdown("🔽 Pour chaque trade, sélectionne l’école, l’edge, le type de trade, l’intervalle de l’edge et observe la session automatiquement détectée.")

# Add columns
for col in ['Session', 'Trade Type', 'Edge Time Frame', 'Risk in Dollars', 'Risk as % of Capital']:
    if col not in df.columns:
        df[col] = "" if "Risk" not in col else 0.0

for i in range(len(df)):
    st.markdown(f"---")
    st.markdown(f"### 🧾 Trade #{i + 1}")
    trade_data = df.iloc[i]
    st.dataframe(trade_data.to_frame().T, hide_index=True)

    open_time_str = trade_data.get("Open Time")
    close_time_str = trade_data.get("Close Time")
    open_price = trade_data.get("Open Price")
    close_price = trade_data.get("Close Price")
    symbol = trade_data.get("Symbol")

    try:
        trade_time = pd.to_datetime(open_time_str, format='%Y.%m.%d %H:%M:%S', errors='coerce')
        if pd.isnull(trade_time):
            raise ValueError("Format invalide")
        session = get_session_from_time(trade_time, st.session_state.timezone)
        df.at[i, 'Session'] = session
    except Exception as e:
        session = "Inconnu"
        st.warning(f"⚠️ Session inconnue pour ce trade #{i + 1}: {e}")

    st.markdown(f"**🕒 Session détectée :** `{session}`")

    col1, col2 = st.columns(2)
    with col1:
        school = st.selectbox("🎓 École", list(edges_dict.keys()), key=f"school_{i}")
    with col2:
        edge = st.selectbox("📌 Edge", edges_dict[school], key=f"edge_{i}")
        if edge == "Autre":
            edge = st.text_input("✍️ Ton edge personnalisé :", key=f"custom_edge_{i}")

    trade_type = st.selectbox("⚡ Type de trade", trade_types, key=f"trade_type_{i}")
    if trade_type == "Autre":
        trade_type = st.text_input("✍️ Ton type de trade personnalisé :", key=f"custom_trade_type_{i}")

    edge_time_frame = st.selectbox("⏱️ Intervalle de l'edge", time_frames, key=f"edge_time_frame_{i}")
    if edge_time_frame == "Autre":
        edge_time_frame = st.text_input("✍️ Ton intervalle personnalisé :", key=f"custom_edge_time_frame_{i}")

    sl_price = trade_data["S / L"]
    volume = trade_data["Volume"]

    contract_size = 100 if symbol == "XAUUSD" else 1 if symbol == "NAS100" else 100000
    price_difference = abs(open_price - sl_price)
    risk_in_dollars = price_difference * volume * contract_size
    risk_as_percentage = (risk_in_dollars / initial_capital) * 100

    df.at[i, 'Risk in Dollars'] = risk_in_dollars
    df.at[i, 'Risk as % of Capital'] = risk_as_percentage
    df.at[i, 'Ecole'] = school
    df.at[i, 'Edge'] = edge
    df.at[i, 'Trade Type'] = trade_type
    df.at[i, 'Edge Time Frame'] = edge_time_frame

    st.markdown(f"**💰 Risque calculé en $ :** `{risk_in_dollars:.2f}`")
    st.markdown(f"**📊 Risque en % du capital initial :** `{risk_as_percentage:.2f}%`")

    plot_paths = plot_trade_chart(i+1, symbol, open_time_str, close_time_str, open_price, close_price)
    if plot_paths:
        for interval, path in plot_paths:
            st.markdown(f"📉 **Graphique {interval}**")
            st.image(path, use_column_width=True)
    else:
        st.warning("❌ Graphiques non disponibles pour ce trade.")

# ----- Save Result -----
st.markdown("### 📊 Trades Annotés avec Session")
st.dataframe(df)

result_dir = "Result"
os.makedirs(result_dir, exist_ok=True)
output_path = os.path.join(result_dir, "trades_annotes.csv")

if st.button("💾 Enregistrer les annotations"):
    df.to_csv(output_path, index=False)
    st.success(f"✅ Fichier annoté enregistré à {output_path}.")
    st.download_button("📥 Télécharger les trades annotés", data=df.to_csv(index=False), file_name="trades_annotes.csv", mime="text/csv")
