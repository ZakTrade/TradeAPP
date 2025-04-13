import streamlit as st
import sqlite3

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

if st.button("Vérifier le symbole"):
    conn, cursor = connect_db()

    # Check if table exists (optional)
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='forex_prices';")
    if not cursor.fetchone():
        st.error("❌ Table 'forex_prices' introuvable.")
    else:
        # Check if the symbol exists in the table
        cursor.execute("SELECT COUNT(*) FROM forex_prices WHERE symbol = ?", (symbol,))
        count = cursor.fetchone()[0]

        if count > 0:
            st.success(f"✅ {count} entrées trouvées pour le symbole `{symbol}` dans la base de données.")
        else:
            st.warning(f"⚠️ Aucun enregistrement trouvé pour `{symbol}`. Vous pouvez maintenant importer des données.")

        # Optional: show 5 most recent rows
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
