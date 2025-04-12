import streamlit as st
import pandas as pd
import pytz
from datetime import datetime
import locale
import platform

# ----- Page Config -----
st.set_page_config(page_title="Trade Reporter - Annotation", layout="wide")
st.title("✍️ Trade Reporter - Étape 2 : Annotation des trades")

# ----- Load uploaded trades -----
try:
    # Check the system's locale and adjust accordingly
    if platform.system() == 'Darwin':  # macOS
        locale.setlocale(locale.LC_NUMERIC, 'fr_FR.UTF-8')  # For macOS locale, adjust accordingly
    else:  # Default to US format for other systems (Windows/Linux)
        locale.setlocale(locale.LC_NUMERIC, 'en_US.UTF-8')

    # Load CSV file
    df = pd.read_csv("data/temp_trades.csv")
except FileNotFoundError:
    st.error("Aucun fichier trouvé. Retourne à l'étape 1 pour uploader ton fichier.")
    st.stop()

# ----- Sidebar: Timezone -----
st.sidebar.header("🕒 Paramètres de fuseau horaire")
timezone = st.sidebar.selectbox("Sélectionne ton fuseau horaire :", pytz.all_timezones, index=pytz.all_timezones.index("Europe/Paris"))

# Store the selected timezone in the session state
if 'timezone' not in st.session_state or st.session_state.timezone != timezone:
    st.session_state.timezone = timezone

# ----- Session Detection Function -----
def get_se
