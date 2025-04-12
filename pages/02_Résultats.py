import streamlit as st
import pandas as pd

# ----- Page Config -----
st.set_page_config(page_title="📊 Performance des Trades", layout="wide")
st.title("📊 Dashboard de Performance des Trades")

# ----- Load Annotated Data -----
try:
    df = pd.read_csv("data/trades_annotés.csv")
except FileNotFoundError:
    st.error("Aucun fichier trouvé. Retourne à l'étape d'annotation pour enregistrer tes trades.")
    st.stop()

# ----- Nettoyage -----
df["Profit"] = pd.to_numeric(df["Profit"], errors="coerce")
df["Risk in Dollars"] = pd.to_numeric(df["Risk in Dollars"], errors="coerce")

# Capital initial saisi
capital_initial = st.number_input("💰 Capital initial (€)", value=1000.0)
df["Capital"] = df["Profit"].cumsum() + capital_initial

# ----- KPIs -----
total_profit = df["Profit"].sum()
avg_profit = df["Profit"].mean()
win_rate = (df["Profit"] > 0).mean() * 100
best_trade = df["Profit"].max()
worst_trade = df["Profit"].min()

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("💹 Profit Total (€)", f"{total_profit:.2f}")
col2.metric("📈 Profit Moyen (€)", f"{avg_profit:.2f}")
col3.metric("✅ Taux de Réussite", f"{win_rate:.1f}%")
col4.metric("🏆 Meilleur Trade", f"{best_trade:.2f} €")
col5.metric("⚠️ Pire Trade", f"{worst_trade:.2f} €")

st.markdown("---")

# ----- Évolution du capital -----
st.subheader("📊 Évolution du Capital")
st.line_chart(df["Capital"])

# ----- Meilleurs / Pires trades -----
st.subheader("🏅 Top 5 Meilleurs Trades")
st.dataframe(df.sort_values(by="Profit", ascending=False).head(5), use_container_width=True)

st.subheader("💥 Top 5 Pires Trades")
st.dataframe(df.sort_values(by="Profit", ascending=True).head(5), use_container_width=True)

st.markdown("---")

# ----- Rentabilité par combinaison -----
st.subheader("🔍 Rentabilité Moyenne par Composante")

def show_profit_table(group_field, title):
    perf = df.groupby(group_field)["Profit"].mean().reset_index().sort_values(by="Profit", ascending=False)
    st.markdown(f"**{title}**")
    st.dataframe(per
