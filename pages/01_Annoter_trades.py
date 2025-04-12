import streamlit as st
import pandas as pd
import pytz
from datetime import datetime

# ----- Page Config -----
st.set_page_config(page_title="Trade Reporter - Annotation", layout="wide")
st.title("✍️ Trade Reporter - Étape 2 : Annotation des trades")

# ----- Load uploaded trades -----
try:
    df = pd.read_csv("data/temp_trades.csv")
except FileNotFoundError:
    st.error("Aucun fichier trouvé. Retourne à l'étape 1 pour uploader ton fichier.")
    st.stop()

# ----- Sidebar: Timezone -----
st.sidebar.header("🕒 Paramètres de fuseau horaire")
timezone = st.sidebar.selectbox("Sélectionne ton fuseau horaire :", pytz.all_timezones, index=pytz.all_timezones.index("Europe/Paris"))

# Store the selected timezone in session_state to maintain it across re-runs
if 'timezone' not in st.session_state or st.session_state.timezone != timezone:
    st.session_state.timezone = timezone

# ----- Session Detection Function -----
def get_session_from_time(trade_time, user_timezone):
    """Calculate the session based on local trade time with dynamic session times."""
    local_tz = pytz.timezone(user_timezone)

    # Define session start and end times in UTC (generic UTC times for sessions)
    sessions = {
        "Asia": {"start": "00:00", "end": "08:00"},      # Asia session
        "London": {"start": "08:00", "end": "13:00"},    # London session
        "New York": {"start": "13:00", "end": "22:00"},  # New York session
        "After Hours": {"start": "22:00", "end": "00:00"} # After Hours session
    }

    # Convert session times to the user's timezone
    session_times = {}
    for session, times in sessions.items():
        # Convert the session start and end times (assumed UTC time) to the user's timezone
        start_time_utc = pytz.utc.localize(datetime.strptime(times["start"], "%H:%M"))
        end_time_utc = pytz.utc.localize(datetime.strptime(times["end"], "%H:%M"))

        # Convert from UTC to the user's selected timezone
        start_time_local = start_time_utc.astimezone(local_tz)
        end_time_local = end_time_utc.astimezone(local_tz)

        session_times[session] = {
            "start": start_time_local,
            "end": end_time_local
        }

    # Check the session based on the local trade time
    for session, times in session_times.items():
        # Check if the trade time falls within the session range
        if times["start"].time() <= trade_time.time() < times["end"].time():
            return session
    return "After Hours"  # Default session if no match found

# ----- Strategy / Edge Mapping -----
edges_dict = {
    "ICT": ["FVG", "OTE", "BOS", "SMT", "Breaker", "Liquidity Sweep", "Judas Swing", "Autre"],
    "SMC": ["CHoCH", "BOS", "FVG", "Order Block", "Liquidity Grab", "Autre"],
    "Wyckoff": ["Spring", "Upthrust", "PSY", "AR", "ST", "LPS", "SOW", "Autre"],
    "Price Action": ["Pin Bar", "Engulfing", "Break & Retest", "Inside Bar", "Autre"],
    "Breakout": ["Breakout Range", "Retest", "Volume Spike", "Autre"],
    "Autre": ["Edge personnalisé"]
}

# ----- Trade Type Options -----
trade_types = ["Scalping", "Swing", "Position", "Day Trading", "Scalp Intraday", "Autre"]

# ----- Edge Time Frame Options -----
time_frames = ["1min", "5min", "15min", "1h", "4h", "D", "W"]

# ----- Display Annotation Interface -----
annotated_data = []

st.markdown("🔽 Pour chaque trade, sélectionne l’école, l’edge, le type de trade, l’intervalle de l’edge et observe la session automatiquement détectée.")

# Add the 'Session', 'Trade Type', and 'Risk' columns for displaying the session and risk
df['Session'] = ""
df['Trade Type'] = ""  # Add new column for trade type
df['Edge Time Frame'] = ""  # Add new column for edge time frame
df['Risk in Dollars'] = 0.0  # Add new column for risk calculation

for i in range(len(df)):
    st.markdown(f"---")
    st.markdown(f"### 🧾 Trade #{i + 1}")

    trade_data = df.iloc[i]
    st.dataframe(trade_data.to_frame().T, hide_index=True)

    # --- Session Detection from "Open Time" column ---
    try:
        open_time_str = trade_data.get("Open Time")  # Corrected to match the 'Open Time' column name

        # Check if open_time is not None or empty
        if pd.isna(open_time_str) or open_time_str.strip() == "":
            raise ValueError(f"Le champ `Open Time` est manquant ou vide pour le trade #{i + 1}.")

        # Parse the open_time with the correct format: 'YYYY.MM.DD HH:MM:SS'
        trade_time = pd.to_datetime(open_time_str, format='%Y.%m.%d %H:%M:%S', errors='coerce')  # Custom format

        if pd.isnull(trade_time):
            raise ValueError(f"Le format de `Open Time` est incorrect pour le trade #{i + 1}. La valeur était : {open_time_str}")

        # Calculate session based on user's selected timezone
        session = get_session_from_time(trade_time, st.session_state.timezone)

        # Add session information to the dataframe
        df.at[i, 'Session'] = session

    except Exception as e:
        session = "Inconnu"
        st.warning(f"⚠️ Impossible de calculer la session pour ce trade #{i + 1}: {e}")

    st.markdown(f"**🕒 Session détectée :** `{session}`")

    # --- École / Edge Inputs ---
    col1, col2 = st.columns(2)
    with col1:
        school = st.selectbox("🎓 École", list(edges_dict.keys()), key=f"school_{i}")
    with col2:
        edge = st.selectbox("📌 Edge", edges_dict[school], key=f"edge_{i}")
        if edge == "Autre":
            edge = st.text_input("✍️ Ton edge personnalisé :", key=f"custom_edge_{i}")

    # --- Trade Type Selection ---
    trade_type = st.selectbox("⚡ Type de trade", trade_types, key=f"trade_type_{i}")
    if trade_type == "Autre":
        trade_type = st.text_input("✍️ Ton type de trade personnalisé :", key=f"custom_trade_type_{i}")

    # --- Edge Time Frame Selection ---
    edge_time_frame = st.selectbox("⏱️ Intervalle de l'edge", time_frames, key=f"edge_time_frame_{i}")
    if edge_time_frame == "Autre":
        edge_time_frame = st.text_input("✍️ Ton intervalle personnalisé :", key=f"custom_edge_time_frame_{i}")

    # --- Risk Calculation ---
    open_price = trade_data["Open Price"]
    sl_price = trade_data["S / L"]
    volume = trade_data["Volume"]
    symbol = trade_data["Symbol"]

    # Calculate Price Difference
    price_difference = abs(open_price - sl_price)

    # Determine Contract Size based on Symbol
    if symbol == "XAUUSD":
        contract_size = 100
    else:
        contract_size = 100000

    # Calculate Risk in Dollars
    risk_in_dollars = price_difference * volume * contract_size
    df.at[i, 'Risk in Dollars'] = risk_in_dollars

    st.markdown(f"**💰 Risque calculé en $ :** `{risk_in_dollars:.2f}`")

    # Add everything to the annotated data
    row_data =
