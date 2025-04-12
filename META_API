import streamlit as st
import MetaTrader5 as mt5
import pandas as pd

# MetaTrader5 initialization
def connect_mt5():
    if not mt5.initialize():
        st.error("MetaTrader 5 initialization failed!")
        return False
    return True

# Function to fetch and display history
def get_trade_history():
    history = mt5.history_orders_get()
    if history is None:
        st.error("No history data available!")
    else:
        history_data = []
        for order in history:
            history_data.append({
                "Ticket": order.ticket,
                "Symbol": order.symbol,
                "Action": order.action,
                "Volume": order.volume,
                "Price": order.price_open,
                "Profit": order.profit,
                "Time": order.time,
            })
        df = pd.DataFrame(history_data)
        st.dataframe(df)

# Streamlit page layout
st.set_page_config(page_title="MetaTrader 5 Trade History", layout="wide")
st.title("📊 MetaTrader 5 Trade History")

# Connect to MT5 when user presses the button
if st.button("Fetch Trade History"):
    if connect_mt5():
        get_trade_history()

# Shut down MetaTrader connection
mt5.shutdown()
