import streamlit as st
import MetaTrader5 as mt5
import sqlite3
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="🏠 Accueil - Connexion MT5", layout="centered")
st.title("🏦 Connexion MetaTrader 5 et Export des Trades")

# ---- DB Setup ----
DB_PATH = "forex_data.db"

def connect_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS trades (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ticket INTEGER,
        symbol TEXT,
        type TEXT,
        volume REAL,
        open_time DATETIME,
        open_price REAL,
        close_time DATETIME,
        close_price REAL,
        profit REAL
    )
    """)
    conn.commit()
    return conn, cursor

# ---- Connect to MT5 ----
st.subheader("🔌 Connexion à MetaTrader 5")

login = st.number_input("Identifiant", step=1)
password = st.text_input("Mot de passe", type="password")
server = st.text_input("Serveur (ex: 'MetaQuotes-Demo')", value="MetaQuotes-Demo")
path = st.text_input("Chemin MT5 (laisser vide pour auto)", value="")

if st.button("Se connecter à MT5"):
    if not mt5.initialize(login=login, password=password, server=server, path=path if path else None):
        st.error(f"❌ Erreur de connexion : {mt5.last_error()}")
    else:
        st.success("✅ Connecté à MT5 avec succès !")

        # ---- Get history ----
        st.subheader("📦 Exporter l'historique des trades")
        orders = mt5.history_deals_get(datetime(2020, 1, 1), datetime.now())

        if orders is None or len(orders) == 0:
            st.warning("Aucun trade trouvé.")
        else:
            df = pd.DataFrame(list(orders), columns=orders[0]._asdict().keys())
            df = df[df['type'] < 2]  # 0 = buy, 1 = sell

            # Clean & rename
            df_clean = pd.DataFrame({
                "ticket": df["ticket"],
                "symbol": df["symbol"],
                "type": df["type"].map({0: "buy", 1: "sell"}),
                "volume": df["volume"],
                "open_time": pd.to_datetime(df["time"]),
                "open_price": df["price"],
                "close_time": pd.to_datetime(df["time_msc"]),
                "close_price": df["price"],
                "profit": df["profit"]
            })

            conn, cursor = connect_db()
            inserted = 0
            for _, row in df_clean.iterrows():
                try:
                    cursor.execute("""
                        INSERT INTO trades (ticket, symbol, type, volume, open_time, open_price, close_time, close_price, profit)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        row["ticket"], row["symbol"], row["type"], row["volume"],
                        row["open_time"], row["open_price"],
                        row["close_time"], row["close_price"],
                        row["profit"]
                    ))
                    inserted += 1
                except:
                    pass
            conn.commit()
            conn.close()

            st.success(f"✅ {inserted} trades insérés dans la base de données.")
            st.dataframe(df_clean.head())
        mt5.shutdown()
