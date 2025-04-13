import sqlite3
import pandas as pd
import mplfinance as mpf
import os

# ----- Configuration -----
DB_PATH = "forex_data.db"  # Replace with your actual DB path
SYMBOLS = ["XAUUSD", "EURUSD", "GBPUSD", "NAS100"]  # Add or remove as needed
TABLE_NAME = "forex_prices"  # Replace if your table name is different

# ----- Connect to Database -----
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Check if table exists
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = [t[0] for t in cursor.fetchall()]
if TABLE_NAME not in tables:
    raise ValueError(f"❌ Table '{TABLE_NAME}' not found in database.")

# ----- Create Output Directory -----
os.makedirs("charts", exist_ok=True)

# ----- Plot Each Symbol -----
for symbol in SYMBOLS:
    print(f"📊 Plotting {symbol}...")

    # Load the data for the symbol
    query = f"""
    SELECT timestamp, open, high, low, close, volume
    FROM {TABLE_NAME}
    WHERE symbol = ?
    ORDER BY timestamp
    """
    df = pd.read_sql_query(query, conn, params=(symbol,))
    
    if df.empty:
        print(f"⚠️ No data found for {symbol}. Skipping.")
        continue

    # Convert timestamp to datetime
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df.set_index('timestamp', inplace=True)

    # Plot and save chart
    chart_file = f"charts/{symbol}_chart.png"
    mpf.plot(df,
             type='candle',
             style='charles',
             title=f"{symbol} Price Chart",
             volume=True,
             mav=(10, 20),
             savefig=chart_file)
    print(f"✅ Saved {symbol} chart to {chart_file}")

# ----- Close connection -----
conn.close()
print("✅ Done.")
