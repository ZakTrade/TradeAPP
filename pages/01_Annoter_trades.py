import sqlite3

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
