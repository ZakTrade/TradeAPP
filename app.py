# app.py
import streamlit as st
import pandas as pd
import os

# ----- Page Config -----
st.set_page_config(page_title="Trade Reporter - Étape 1 : Upload des Trades", layout="wide")
st.title("📂 Trade Reporter - Étape 1 : Upload des Trades")

# ----- File Upload -----
st.sidebar.header("🔽 Télécharge ton fichier CSV de trades")

# Let the user upload a file
uploaded_file = st.sidebar.file_uploader("Choisir un fichier CSV", type=["csv"])

# If a file is uploaded, save it temporarily and navigate to the next step
if uploaded_file is not None:
    # Save the uploaded CSV file to a temporary location
    os.makedirs("data", exist_ok=True)  # Ensure the directory exists
    file_path = os.path.join("data", "temp_trades.csv")

    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.success(f"📈 Fichier `{uploaded_file.name}` téléchargé avec succès.")

    # Provide a button to navigate to the next step (Trade annotation)
    if st.button("👉 Passer à l'étape 2 : Annotation des trades"):
        st.session_state.uploaded_file_path = file_path
        st.experimental_rerun()  # Rerun to go to the next page

else:
    st.warning("⚠️ Aucune fichier téléchargé. Veuillez télécharger un fichier CSV de trades.")
