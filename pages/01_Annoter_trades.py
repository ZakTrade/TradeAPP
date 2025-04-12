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
    """Calculate the session based on local trade time"""
    local_tz = pytz.timezone(user_timezone)
    # Localize the trade time based on the selected user's timezone
    trade_time_local = local_tz.localize(trade_time)

    # Check the session based on the local time
    if 0 <= trade_time_local.hour < 8:
        return "Asia"
    elif 8 <= trade_time_local.hour < 13:
        return "London"
    elif 13 <= trade_time_local.hour < 22:
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

# Add the 'Session' column for displaying the session
df['Session'] = ""

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

    # Add everything to the annotated data
    row_data = trade_data.to_dict()
    row_data["Ecole"] = school
    row_data["Edge"] = edge
    row_data["Session"] = session
    annotated_data.append(row_data)

# ----- Display the DataFrame with 'Session' column -----
st.markdown("### 📊 Trades Annotés avec Session")
st.dataframe(df)

# ----- Save and Export -----
st.markdown("---")
if st.button("💾 Enregistrer les annotations"):
    annotated_df = pd.DataFrame(annotated_data)
    annotated_df.to_csv("data/trades_annotés.csv", index=False)
    st.success("✅ Fichier annoté enregistré avec succès.")
    st.download_button("📥 Télécharger les trades annotés",
                       data=annotated_df.to_csv(index=False),
                       file_name="trades_annotes.csv",
                       mime="text/csv")
