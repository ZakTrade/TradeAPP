import streamlit as st
import pandas as pd

st.set_page_config(page_title="Trade Reporter - Annotation", layout="wide")
st.title("✍️ Trade Reporter - Étape 2 : Annotation des trades")

# Load uploaded CSV
try:
    df = pd.read_csv("data/temp_trades.csv")
except FileNotFoundError:
    st.error("Aucun fichier trouvé. Retourne à l'étape 1 pour uploader ton fichier.")
    st.stop()

st.markdown("🔽 Pour chaque trade, sélectionne l’école et l’edge utilisé.")

# Edge options by school
edges_dict = {
    "ICT": ["FVG", "OTE", "BOS", "SMT", "Breaker", "Liquidity Sweep", "Judas Swing", "Autre"],
    "SMC": ["CHoCH", "BOS", "FVG", "Order Block", "Liquidity Grab", "Autre"],
    "Wyckoff": ["Spring", "Upthrust", "PSY", "AR", "ST", "LPS", "SOW", "Autre"],
    "Price Action": ["Pin Bar", "Engulfing", "Break & Retest", "Inside Bar", "Autre"],
    "Breakout": ["Breakout Range", "Retest", "Volume Spike", "Autre"],
    "Autre": ["Edge personnalisé"]
}

# Prepare annotated data
annotated_data = []

# Iterate all trades
for i in range(len(df)):
    st.markdown(f"---")
    st.markdown(f"**🧾 Trade #{i + 1}**")
    
    trade_data = df.iloc[i]
    st.write(trade_data.to_frame().T)  # Display the row as a one-row table

    # Select strategy/school
    school = st.selectbox("🎓 École", list(edges_dict.keys()), key=f"school_{i}")
    
    # Select edge
    edge_options = edges_dict[school]
    edge = st.selectbox("📌 Edge", edge_options, key=f"edge_{i}")
    
    # Custom edge if needed
    if edge == "Autre":
        edge = st.text_input("✍️ Ton edge personnalisé :", key=f"custom_edge_{i}")

    # Save this row
    row_data = trade_data.to_dict()
    row_data["Ecole"] = school
    row_data["Edge"] = edge
    annotated_data.append(row_data)

# Save all annotated trades
st.markdown("---")
if st.button("💾 Sauvegarder les annotations"):
    annotated_df = pd.DataFrame(annotated_data)
    annotated_df.to_csv("data/trades_annotés.csv", index=False)
    st.success("✅ Fichier annoté enregistré avec succès.")
    st.download_button("📥 Télécharger les trades annotés",
                       data=annotated_df.to_csv(index=False),
                       file_name="trades_annotes.csv",
                       mime="text/csv")
