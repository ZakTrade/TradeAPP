import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime
import requests
from io import StringIO

# ---- Page Config ----
st.set_page_config(page_title="📊 Forex DB Check", layout="centered")
st.title("🧪 Vérification de la base de données Forex")

# ---- Connect to DB & Setup ----
DB_PATH = "forex_data.db"

def connect_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Create table if not exists
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS forex_prices (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        symbol TEXT NOT NULL,
        timestamp DATETIME NOT NULL,
        open REAL,
        high REAL,
        low REAL,
        close REAL,
        volume REAL
    )
    """)
    conn.commit()
    return conn, cursor

# ---- UI ----
symbol = st.text_input("🔍 Entrez un symbole (ex: XAUUSD, EURUSD, NAS100)", "XAUUSD").upper()

# ---- CSV Upload ----
st.subheader("📤 Importer des données Forex")
uploaded_file = st.file_uploader("Choisissez un fichier CSV contenant les données du symbole spécifié", type=["csv"])

def insert_data_from_df(df, symbol):
    conn, cursor = connect_db()
    inserted = 0
    for _, row in df.iterrows():
        try:
            cursor.execute("""
                INSERT INTO forex_prices (symbol, timestamp, open, high, low, close, volume)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                symbol,
                datetime.strptime(str(row["timestamp"]), "%Y-%m-%d %H:%M:%S"),
                row["open"], row["high"], row["low"], row["close"], row["volume"]
            ))
            inserted += 1
        except Exception as e:
            st.warning(f"Erreur lors de l'insertion d'une ligne : {e}")
    conn.commit()
    conn.close()
    return inserted

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
        st.write("Aperçu du fichier :")
        st.dataframe(df.head())

        required_cols = {"timestamp", "open", "high", "low", "close", "volume"}
        if not required_cols.issubset(set(df.columns)):
            st.error(f"Le fichier doit contenir les colonnes suivantes : {required_cols}")
        else:
            inserted = insert_data_from_df(df, symbol)
            st.success(f"✅ {inserted} lignes insérées pour `{symbol}` dans la base de données.")
    except Exception as e:
        st.error(f"Erreur lors de la lecture du fichier : {e}")

# ---- Get Data from ForexSB ----
st.subheader("🌐 Télécharger des données depuis ForexSB")
fetch_symbols = ["XAUUSD", "EURUSD", "GBPUSD", "NAS100"]
periods = ["M1", "M5", "M15", "H1"]

if st.button("⬇️ Télécharger et insérer les données ForexSB"):
    base_url = "https://forexsb.com/historical-data/download/"

    for s in fetch_symbols:
        for p in periods:
            st.write(f"🔄 Téléchargement {s} ({p})...")
            try:
                url = f"{base_url}{s.lower()}-{p}.csv"
                response = requests.get(url)
                if response.status_code == 200:
                    df = pd.read_csv(StringIO(response.text))
                    df.columns = [c.lower() for c in df.columns]
                    if "time" in df.columns:
                        df.rename(columns={"time": "timestamp"}, inplace=True)
                    inserted = insert_data_from_df(df, s)
                    st.success(f"✅ {inserted} lignes insérées pour {s} ({p})")
                else:
                    st.warning(f"⚠️ Données introuvables pour {s} ({p})")
            except Exception as e:
                st.error(f"❌ Erreur lors du téléchargement pour {s} ({p}) : {e}")

# ---- Check Existing Data ----
if st.button("📌 Vérifier le symbole dans la base"):
    conn, cursor = connect_db()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='forex_prices';")
    if not cursor.fetchone():
        st.error("❌ Table 'forex_prices' introuvable.")
    else:
        cursor.execute("SELECT COUNT(*) FROM forex_prices WHERE symbol = ?", (symbol,))
        count = cursor.fetchone()[0]

        if count > 0:
            st.success(f"✅ {count} entrées trouvées pour le symbole `{symbol}` dans la base de données.")
        else:
            st.warning(f"⚠️ Aucun enregistrement trouvé pour `{symbol}`. Vous pouvez maintenant importer des données.")

        cursor.execute("""
        SELECT timestamp, open, high, low, close, volume
        FROM forex_prices
        WHERE symbol = ?
        ORDER BY timestamp DESC
        LIMIT 5
        """, (symbol,))
        rows = cursor.fetchall()

        if rows:
            st.subheader("📈 Dernières entrées pour ce symbole")
            st.dataframe(rows, use_container_width=True)
        else:
            st.info("📭 Aucun échantillon de données à afficher.")

    conn.close()
