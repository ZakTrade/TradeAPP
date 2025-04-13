import streamlit as st
import pandas as pd
import os

# --- Page Configuration ---
st.set_page_config(page_title="Trade Reporter - Upload", layout="centered")
st.title("📊 Trade Reporter - Étape 1 : Import des trades")

# --- Formulaire principal ---
st.subheader("⚙️ Paramètres généraux")

# Trader name and capital input
trader_name = st.text_input("Nom du trader", "TraderX")
capital = st.number_input("Capital initial (€)", min_value=100.0, value=1000.0)

# Upload the CSV file
uploaded_file = st.file_uploader("📂 Upload ton fichier de trades (.csv)", type="csv")

# --- Handling file upload and number format issue ---
if uploaded_file is not None:
    # Read the file into a dataframe
    df = pd.read_csv(uploaded_file)

    # Detect if the file has numbers with commas (likely Mac/European format)
    if df.select_dtypes(include='object').apply(lambda col: col.str.contains(',', na=False)).any().any():
        # Replace commas with dots in numeric columns
        df = df.applymap(lambda x: str(x).replace(',', '.') if isinstance(x, str) else x)

    # Try to convert all columns to numeric where applicable
    for col in df.select_dtypes(include='object').columns:
        df[col] = pd.to_numeric(df[col], errors='ignore')  # Ignore non-convertible columns

    # Show success message and the first few rows
    st.success("✅ Fichier chargé avec succès !")
    st.dataframe(df.head())

    # Save the file temporarily for use in the next page
    os.makedirs("data", exist_ok=True)  # Ensure the 'data' directory exists
    df.to_csv("data/temp_trades.csv", index=False)

    # Provide a link to the next page for annotation
    st.markdown("➡️ Passe à l'étape suivante pour annoter tes trades.")
    st.page_link("pages/01_Annoter_trades.py", label="🚀 Annoter les trades", icon="✍️")
else:
    st.info("Upload ton fichier pour activer l'étape suivante.")
