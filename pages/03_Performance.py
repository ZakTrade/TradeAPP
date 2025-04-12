import streamlit as st
import pandas as pd
import os

# ----- Page Config -----
st.set_page_config(page_title="Trade Reporter - KPIs", layout="wide")
st.title("📈 Trade Reporter - Étape 3 : KPIs de Performance")

# ----- Load Annotated Trades -----
file_path = "Result/trades_annotes.csv"
if not os.path.exists(file_path):
    st.error("Aucun fichier de trades annotés trouvé. Retourne à l'étape 2 pour annoter les trades.")
    st.stop()

df = pd.read_csv(file_path)

# ----- Basic Stats -----
st.header("📊 Statistiques Générales")

if 'Profit' not in df.columns:
    st.warning("⚠️ La colonne `Profit` est absente. Assure-toi qu'elle existe dans tes données.")
else:
    total_trades = len(df)
    winning_trades = df[df['Profit'] > 0]
    losing_trades = df[df['Profit'] <= 0]

    win_rate = (len(winning_trades) / total_trades) * 100 if total_trades else 0
    avg_profit = df['Profit'].mean()
    total_profit = df['Profit'].sum()

    profit_factor = (
        winning_trades['Profit'].sum() / abs(losing_trades['Profit'].sum())
        if not losing_trades.empty else float('inf')
    )

    avg_risk_pct = df['Risk as % of Capital'].mean()

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("📈 Total Trades", total_trades)
    col2.metric("✅ Win Rate", f"{win_rate:.2f}%")
    col3.metric("💰 Total Profit", f"{total_profit:.2f}")
    col4.metric("🧮 Profit Factor
