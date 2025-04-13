# fetch_forex_data.py
import yfinance as yf
import sqlite3
import datetime


# Connect to the database
conn = sqlite3.connect("forex_data.db")
cursor = conn.cursor()

# Check tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

print("✅ Tables found:", tables)

# Optional: Check table schema
cursor.execute("PRAGMA table_info(forex_prices);")
columns = cursor.fetchall()

print("\n🧱 Table structure:")
for col in columns:
    print(col)

conn.close()
symbols = {
    "XAUUSD": "XAUUSD=X",  # Gold
    "EURUSD": "EURUSD=X",
    "GBPUSD": "GBPUSD=X",
    "NAS100": "^NDX"       # Nasdaq 100 Index
}

def fetch_and_store():
    conn = sqlite3.connect("forex_data.db")
    cursor = conn.cursor()

    for symbol_name, y_symbol in symbols.items():
        df = yf.download(y_symbol, period="7d", interval="1h")  # change as needed
        for index, row in df.iterrows():
            cursor.execute("""
                INSERT INTO forex_prices (symbol, timestamp, open, high, low, close, volume)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                symbol_name,
                index.to_pydatetime(),
                row['Open'],
                row['High'],
                row['Low'],
                row['Close'],
                row['Volume']
            ))

    conn.commit()
    conn.close()

fetch_and_store()
✅ Tables found: [('forex_prices',)]

🧱 Table structure:
(0, 'id', 'INTEGER', 0, None, 1)
(1, 'symbol', 'TEXT', 1, None, 0)
(2, 'timestamp', 'DATETIME', 1, None, 0)
(3, 'open', 'REAL', 0, None, 0)
(4, 'high', 'REAL', 0, None, 0)
(5, 'low', 'REAL', 0, None, 0)
(6, 'close', 'REAL', 0, None, 0)
(7, 'volume', 'REAL', 0, None, 0)
