import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Trade Reporter - Performance", layout="wide")
st.title("📈 Analyse de Performance des Trades")

# Chargement du fichier annoté
try:
    df = pd.read_csv("data/trades_annotés.csv")
except FileNotFoundError:
    st.error("Aucun fichier annoté trouvé. Retourne à l'étape 2 pour annoter tes trades.")
    st.stop()

# Vérifiez les colonnes existantes dans le DataFrame
st.write("Colonnes disponibles dans le DataFrame :")
st.write(df.columns)

# Nettoyage des données
df["Profit"] = pd.to_numeric(df["Profit"], errors="coerce").fillna(0)
df["Close Time"] = pd.to_datetime(df["Close Time"], format="%Y.%m.%d %H:%M:%S", errors="coerce")

# Calcul du solde cumulé
df = df.sort_values("Close Time")
df["Balance"] = df["Profit"].cumsum()

# Affichage de l'évolution du solde
st.subheader("📊 Évolution du solde")
fig = px.line(df, x="Close Time", y="Balance", title="Évolution du capital")
st.plotly_chart(fig, use_container_width=True)

# Calcul et affichage des KPIs
total_profit = df["Profit"].sum()
avg_profit = df["Profit"].mean()
win_rate = (df[df["Profit"] > 0].shape[0] / df.shape[0]) * 100

st.subheader("📊 Indicateurs Clés de Performance (KPIs)")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Profit Total (€)", f"{total_profit:.2f}")
with col2:
    st.metric("Profit Moyen par Trade (€)", f"{avg_profit:.2f}")
with col3:
    st.metric("Taux de Réussite (%)", f"{win_rate:.2f}")

# Vérification des 5 meilleurs et 5 pires trades
st.subheader("🏆 Meilleurs et Pires Trades")
col1, col2 = st.columns(2)

# Assurez-vous que les colonnes nécessaires existent avant de tenter de les utiliser
if set(["Profit", "Symbol", "Session", "Ecole", "Edge"]).issubset(df.columns):
    with col1:
        st.markdown("**💹 Top 5 Profits**")
        st.dataframe(df.nlargest(5, "Profit")[["Symbol", "Profit", "Session", "Ecole", "Edge"]])

    with col2:
        st.markdown("**📉 Top 5 Pertes**")
        st.dataframe(df.nsmallest(5, "Profit")[["Symbol", "Profit", "Session", "Ecole", "Edge"]])
else:
    st.error("Certaines colonnes nécessaires ('Symbol', 'Profit', 'Session', 'Ecole', 'Edge') sont manquantes dans le DataFrame.")

# Analyse de rentabilité par combinaison
st.subheader("🔍 Synthèse des combinaisons les plus rentables")
group_cols = ["Session", "Edge Time Frame", "Ecole", "Edge", "Trade Type"]
grouped = df.groupby(group_cols)["Profit"].sum().reset_index()
grouped = grouped.sort_values(by="Profit", ascending=False)

st.markdown("**💡 Top 10 Combinaisons Rentables**")
st.dataframe(grouped.head(10))
