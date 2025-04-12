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
timezone = st.sidebar.selectbox("Ton fuseau horaire :", pytz.all_timezones, index=pytz.all_timezones.index("Europe/Paris"))

# ----- Session Detection Function -----
def get_session_from_utc(utc_time):
    if 0 <= utc_time.hour < 8:
        return "Asia"
    elif 8 <= utc_time.hour < 13:
        return "London"
    elif 13 <= utc_time.hour < 22:
        return "New York"
    else:
        return "After Hours"

# ----- Strategy / Edge Mapping -----
edges_dict = {
    "ICT": ["FVG", "OTE", "BOS", "SMT", "Breaker", "Liquidity Sweep", "Judas Swing", "Autre"],
    "SMC": ["CHoCH", "BOS", "FVG", "Order Block", "Liquidity Grab", "Autre"],
    "Wyckoff": ["Spring", "Upthrust", "PSY", "AR", "ST", "LPS", "SOW", "Autre"],
    "Price Action": ["Pin Bar", "Engulfing", "Break & Retest", "Inside Bar", "Autre"],
    "Breakout": ["Breakout Range", "Retest", "Volume Spike", "Autre"],
    "Autre": ["Edge personnalisé"]
}

# ----- Display Annotation Interface -----
annotated_data = []

st.markdown("🔽 Pour chaque trade, sélectionne l’école, l’edge, et observe la session automatiquement détectée.")

for i in range(len(df)):
    st.markdown(f"---")
    st.markdown(f"### 🧾 Trade #{i + 1}")

    trade_data = df.iloc[i]
    st.dataframe(trade_data.to_frame().T, hide_index=True)

    # --- Session Detection from "open_time" column ---
    try:
        open_time_str = trade_data.get("open_time")  # Ensure this matches your column name
        local_tz = pytz.timezone(timezone)
        open_time_local = local_tz.localize(datetime.strptime(open_time_str, "%Y-%m-%d %H:%M:%S"))
        open_time_utc = open_time_local.astimezone(pytz.utc)
        session = get_session_from_utc(open_time_utc)
    except Exception as e:
        session = "Inconnu"
        st.warning(f"⚠️ Impossible de calculer la session pour ce trade : {e}")

    st.markdown(f"**🕒 Session détectée :** `{ses
