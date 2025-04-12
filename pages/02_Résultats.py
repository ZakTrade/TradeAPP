import streamlit as st
import pandas as pd

# ----- Page Config -----
st.set_page_config(page_title="Trade Reporter - Résultats", layout="wide")
st.title("📈 Résultats des trades annotés")

# ----- Load Annotated Data -----
try:
    df = pd.read_csv("data/trades_annotés.csv")
except FileNotFoundError:
    st.error("Aucun fichier de résultats trouvé. Assure-toi d’avoir terminé l’annotation.")
    st.stop()

# ----- Custom CSS Styles -----
def colorize_column(val, col_name):
    color_map = {
        "Session": {"Asia": "#D6EAF8", "London": "#D5F5E3", "New York": "#F9E79F", "After Hours": "#FADBD8", "Inconnu": "#F2F3F4"},
        "Trade Type": {"Scalping": "#FEF9E7", "Swing": "#FDEDEC", "Position": "#EBF5FB", "Day Trading": "#E8F8F5", "Scalp Intraday": "#F6DDCC"},
        "Edge Time Frame": {"1min": "#D1F2EB", "5min": "#FCF3CF", "15min": "#E8DAEF", "1h": "#D6EAF8", "4h": "#F9EBEA", "D": "#FDEBD0", "W": "#F5EEF8"}
    }

    color = color_map.get(col_name, {}).get(val, "#FFFFFF")
    return f"background-color: {color}"

# ----- Styling Function -----
def style_dataframe(df):
    styled_df = df.style \
        .applymap(lambda val: colorize_column(val, "Session"), subset=["Session"]) \
        .applymap(lambda val: colorize_column(val, "Trade Type"), subset=["Trade Type"]) \
        .applymap(lambda val: colorize_column(val, "Edge Time Frame"), subset=["Edge Time Frame"])
    return styled_df

# ----- Display Data -----
st.markdown("### 📋 Aperçu des résultats annotés")
st.dataframe(style_dataframe(df), use_container_width=True)
