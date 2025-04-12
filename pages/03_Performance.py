import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Trade Reporter - Performance", layout="wide")
st.title("📈 Analyse de Performance des Trades")

# Chargement du fichier annoté
try:
    df = pd.read_csv("data/trades_annotés.csv")
except FileNotFoundError:
    st.error("Aucun fichier annoté trouvé. Retourne à l'étape 2 pour annoter tes trades.")
    st.stop()

# Nettoyage
df["Profit"] = pd.to_numeric(df["Profit"], errors="coerce").fillna(0)
df["Close Time"] = pd.to_datetime(df["Close Time"], format="%Y.%m.%d %H:%M:%S", errors="coerce")

# Calcul du solde cumulé
df = df.sort_values("Close Time")
df["Balance"] = df["Profit"].cumsum()

# Affichage de l'évolution du solde
st.subheader("📊 Évolution du solde")
fig, ax = plt.subplots(figsize=(10, 4))
sns.lineplot(data=df, x="Close Time", y="Balance", ax=ax)
ax.set_xlabel("Date")
ax.set_ylabel("Solde (€)")
ax.set_title("Évolution du capital")
st.pyplot(fig)

# Top 5 meilleurs et pires trades
st.subheader("🏆 Meilleurs et Pires Trades")
col1, col2 = st.columns(2)

with col1:
    st.markdown("**💹 Top 5 Profits**")
    st.dataframe(df.nlargest(5, "Profit")[["Symbol", "Profit", "Session", "Ecole", "Edge"]])

with col2:
    st.markdown("**📉 Top 5 Pertes**")
    st.dataframe(df.nsmallest(5, "Profit")[["Symbol", "Profit", "Session", "Ecole", "Edge"]])

# Analyse de rentabilité par combinaison
st.subheader("🔍 Synthèse des combinaisons les plus rentables")

group_cols = ["Session", "Edge Time Frame", "Ecole", "Edge", "Trade Type"]
grouped = df.groupby(group_cols)["Profit"].sum().reset_index()
grouped = grouped.sort_values(by="Profit", ascending=False)

st.markdown("**💡 Top 10 Combinaisons Rentables**")
st.dataframe(grouped.head(10))

# Heatmap des sessions vs rentabilité
st.subheader("🌍 Rentabilité par Session")
session_profit = df.groupby("Session")["Profit"].sum().sort_values(ascending=False)
st.bar_chart(session_profit)
