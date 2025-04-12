import streamlit as st
import pandas as pd
import plotly.express as px

# ----- Page Config -----
st.set_page_config(page_title="📊 Performance des Trades", layout="wide")
st.title("📊 Dashboard de Performance des Trades")

# ----- Load Annotated Data -----
try:
    df = pd.read_csv("data/trades_annotés.csv")
except FileNotFoundError:
    st.error("Aucun fichier trouvé. Retourne à l'étape d'annotation pour enregistrer tes trades.")
    st.stop()

# ----- Nettoyage & Préparation -----
df["Profit"] = pd.to_numeric(df["Profit"], errors="coerce")
df["Risk in Dollars"] = pd.to_numeric(df["Risk in Dollars"], errors="coerce")

# Calcul de l’évolution du capital
capital_initial = st.number_input("💰 Capital initial (€)", value=1000.0)
df["Capital"] = df["Profit"].cumsum() + capital_initial

# KPI Zone
total_profit = df["Profit"].sum()
avg_profit = df["Profit"].mean()
win_rate = (df["Profit"] > 0).mean() * 100
best_trade = df["Profit"].max()
worst_trade = df["Profit"].min()

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("💹 Profit Total (€)", f"{total_profit:.2f}")
col2.metric("📈 Profit Moyen (€)", f"{avg_profit:.2f}")
col3.metric("✅ Taux de Réussite", f"{win_rate:.2f}%")
col4.metric("🏆 Meilleur Trade (€)", f"{best_trade:.2f}")
col5.metric("⚠️ Pire Trade (€)", f"{worst_trade:.2f}")

st.markdown("---")

# ----- Graphique : Évolution du Capital -----
st.subheader("📊 Évolution du Capital")
fig = px.line(df, y="Capital", title="Évolution du capital au fil des trades")
st.plotly_chart(fig, use_container_width=True)

# ----- Meilleurs et Pires trades -----
st.subheader("🏅 Top 5 des meilleurs trades")
st.dataframe(df.sort_values(by="Profit", ascending=False).head(5), use_container_width=True)

st.subheader("💥 Top 5 des pires trades")
st.dataframe(df.sort_values(by="Profit", ascending=True).head(5), use_container_width=True)

st.markdown("---")

# ----- Analyse de rentabilité par combinaison -----
st.subheader("🔍 Analyse de rentabilité par combinaison")

# Par session
session_perf = df.groupby("Session")["Profit"].mean().reset_index().sort_values(by="Profit", ascending=False)
st.markdown("**📆 Par Session**")
st.dataframe(session_perf)

# Par Edge Time Frame
timeframe_perf = df.groupby("Edge Time Frame")["Profit"].mean().reset_index().sort_values(by="Profit", ascending=False)
st.markdown("**⏱️ Par Edge Time Frame**")
st.dataframe(timeframe_perf)

# Par Trade Type
type_perf = df.groupby("Trade Type")["Profit"].mean().reset_index().sort_values(by="Profit", ascending=False)
st.markdown("**⚡ Par Type de Trade**")
st.dataframe(type_perf)

# Par École
school_perf = df.groupby("Ecole")["Profit"].mean().reset_index().sort_values(by="Profit", ascending=False)
st.markdown("**🎓 Par École**")
st.dataframe(school_perf)

# Par Edge
edge_perf = df.groupby("Edge")["Profit"].mean().reset_index().sort_values(by="Profit", ascending=False)
st.markdown("**📌 Par Edge**")
st.dataframe(edge_perf)

# ----- Rentabilité par % de risque -----
df["Risk %"] = df["Risk in Dollars"] / capital_initial * 100
risk_buckets = pd.cut(df["Risk %"], bins=[0, 0.5, 1, 2, 5, 10, 100], include_lowest=True)
risk_perf = df.groupby(risk_buckets)["Profit"].mean().reset_index().rename(columns={"Risk %": "Risk Range"})
st.markdown("**📉 Rentabilité selon le pourcentage de risque**")
st.dataframe(risk_perf)

# ----- Fin -----
st.success("✅ Dashboard généré avec succès.")
