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
