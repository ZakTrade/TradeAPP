import streamlit as st
import pandas as pd

st.set_page_config(page_title="Trade Reporter - Annotation", layout="wide")
st.title("✍️ Trade Reporter - Étape 2 : Annotation des trades")

# Chargement du fichier CSV temporaire
try:
    df = pd.read_csv("data/temp_trades.csv")
except FileNotFoundError:
    st.error("Aucun fichier trouvé. Retourne à l'étape 1 pour uploader ton fichier.")
    st.stop()

st.markdown("🔽 Annoter chaque trade avec l’école (stratégie) et l’edge utilisé.")

# Dictionnaire des edges par école
edges_dict = {
    "ICT": ["FVG", "OTE", "BOS", "SMT", "Breaker", "Liquidity Sweep", "Judas Swing", "Autre"],
    "SMC": ["CHoCH", "BOS", "FVG", "Order Block", "Liquidity Grab", "Autre"],
    "Wyckoff": ["Spring", "Upthrust", "PSY", "AR", "ST", "LPS", "SOW", "Autre"],
    "Price Action": ["Pin Bar", "Engulfing", "Break & Retest", "Inside Bar", "Autre"],
    "Breakout": ["Breakout Range", "Retest", "Volume Spike", "Autre"],
    "Autre": ["Edge personnalisé"]
}

# Création des nouvelles colonnes dans la DataFrame
df["Ecole"] = ""
df["Edge"] = ""

annotated_data = []

st.write("👇 Complète chaque ligne :")

for i in range(len(df)):
    row = df.iloc[i]
    st.markdown(f"---")
    st.markdown(f"**Trade #{i+1}** – Instrument: `{row.get('instrument', 'inconnu')}`")

    # Affichage des infos du trade
    cols = st.columns(df.shape[1] - 2)  # -2 because we're adding Ecole & Edge

    for j, column in enumerate(df.columns[:-2]):  # Show existing data
        with cols[j]:
            st.markdown(f"**{column}**")
            st.write(row[column])

    col_school, col_edge = st.columns(2)

    with col_school:
        school = st.selectbox("🎓 École", list(edges_dict.keys()), key=f"school_{i}")
    with col_edge:
        edge_options = edges_dict.get(school, ["Autre"])
        edge = st.selectbox("📌 Edge", edge_options, key=f"edge_{i}")
        if edge == "Autre":
            edge = st.text_input("✍️ Edge personnalisé", key=f"custom_edge_{i}")

    # Ajout dans la nouvelle ligne annotée
    annotated_row = row.to_dict()
    annotated_row["Ecole"] = school
    annotated_row["Edge"] = edge
    annotated_data.append(annotated_row)

# Sauvegarde
st.markdown("---")
if st.button("💾 Enregistrer les annotations"):
    annotated_df = pd.DataFrame(annotated_data)
    annotated_df.to_csv("data/trades_annotés.csv", index=False)
    st.success("✅ Fichier annoté enregistré avec succès.")
    st.download_button("📥 Télécharger les trades annotés",
                       data=annotated_df.to_csv(index=False),
                       file_name="trades_annotes.csv",
                       mime="text/csv")
