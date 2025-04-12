import streamlit as st
import pandas as pd

st.set_page_config(page_title="Trade Reporter - Annotation", layout="wide")
st.title("✍️ Trade Reporter - Étape 2 : Annotation des trades")

# Chargement du fichier temporaire
try:
    df = pd.read_csv("data/temp_trades.csv")
except FileNotFoundError:
    st.error("Aucun fichier trouvé. Retourne à l'étape 1 pour uploader ton fichier.")
    st.stop()

# Écoles et edges
edges_dict = {
    "ICT": ["FVG", "OTE", "BOS", "SMT", "Breaker", "Liquidity Sweep", "Judas Swing", "Autre"],
    "SMC": ["CHoCH", "BOS", "FVG", "Order Block", "Liquidity Grab", "Autre"],
    "Wyckoff": ["Spring", "Upthrust", "PSY", "AR", "ST", "LPS", "SOW", "Autre"],
    "Price Action": ["Pin Bar", "Engulfing", "Break & Retest", "Inside Bar", "Autre"],
    "Breakout": ["Breakout Range", "Retest", "Volume Spike", "Autre"],
    "Autre": ["Edge personnalisé"]
}

st.markdown("🔽 Choisis l’école et le edge pour chaque trade :")

# Pour chaque ligne, on affiche un petit formulaire
annotated_data = []

for index, row in df.iterrows():
    with st.expander(f"Trade #{index + 1} – {row.get('instrument', 'instrument inconnu')}"):
        col1, col2 = st.columns([1, 2])
        
        with col1:
            school = st.selectbox(f"École #{index+1}", list(edges_dict.keys()), key=f"school_{index}")
        
        with col2:
            edge = st.selectbox(f"Edge utilisé #{index+1}", edges_dict[school], key=f"edge_{index}")
            if edge == "Autre":
                edge = st.text_input("Edge personnalisé :", key=f"custom_edge_{index}")

        # Ajouter les annotations aux données
        annotated_row = row.to_dict()
        annotated_row["Ecole"] = school
        annotated_row["Edge"] = edge
        annotated_data.append(annotated_row)

# Bouton pour enregistrer
if st.button("💾 Sauvegarder les trades annotés"):
    annotated_df = pd.DataFrame(annotated_data)
    annotated_df.to_csv("data/trades_annotés.csv", index=False)
    st.success("✅ Trades annotés enregistrés avec succès !")
    st.download_button("📥 Télécharger le fichier annoté", data=annotated_df.to_csv(index=False), file_name="trades_annotes.csv")
