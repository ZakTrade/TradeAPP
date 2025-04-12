import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Trade Reporter - Upload", layout="centered")
st.title("📊 Trade Reporter - Étape 1 : Import des trades")

# Formulaire principal
st.subheader("⚙️ Paramètres généraux")

trader_name = st.text_input("Nom du trader", "TraderX")
capital = st.number_input("Capital initial (€)", min_value=100.0, value=1000.0)

uploaded_file = st.file_uploader("📂 Upload ton fichier de trades (.csv)", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    st.success("✅ Fichier chargé avec succès !")
    st.dataframe(df.head())

    # On sauvegarde le fichier temporairement pour l’utiliser dans la 2e page
    df.to_csv("data/temp_trades.csv", index=False)

    st.markdown("➡️ Passe à l'étape suivante pour annoter tes trades.")
    st.page_link("pages/01_Annoter_trades.py", label="🚀 Annoter les trades", icon="✍️")
else:
    st.info("Upload ton fichier pour activer l'étape suivante.")
