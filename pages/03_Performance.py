import streamlit as st
import pandas as pd
import os

# ----- Page Config -----
st.set_page_config(page_title="Performance Report", layout="wide")
st.title("📈 Performance Report")

# Path to the CSV file in the /Result/ directory
csv_file_path = "Result/trades_annotes.csv"

# Check if the file exists
if os.path.exists(csv_file_path):
    # Load the CSV file into a DataFrame
    df = pd.read_csv(csv_file_path)
    
    # ----- Display Summary Statistics -----
    st.markdown("### 🔎 Performance Summary")
    
    # Display total profit and total trades
    total_profit = df['Profit'].sum()
    total_trades = len(df)
    
    st.markdown(f"**Total Profit:** {total_profit:.2f}")
    st.markdown(f"**Total Number of Trades:** {total_trades}")
    
    # ----- Best and Worst Trades -----
    best_trade = df.loc[df['Profit'].idxmax()]
    worst_trade = df.loc[df['Profit'].idxmin()]
    
    st.markdown("### 🏆 Best Trade")
    st.write(best_trade)
    
    st.markdown("### 💔 Worst Trade")
    st.write(worst_trade)
    
    # ----- Performance by Edge -----
    st.markdown("### 📊 Performance by Edge")
    
    # Group by 'Edge' and calculate average profit per edge
    edge_performance = df.groupby('Edge')['Profit'].mean().sort_values(ascending=False)
    st.write(edge_performance)
    
    # ----- Performance by 'Ecole' -----
    st.markdown("### 📊 Performance by Ecole")
    
    # Group by 'Ecole' and calculate average profit per school
    ecole_performance = df.groupby('Ecole')['Profit'].mean().sort_values(ascending=False)
    st.write(ecole_performance)
    
    # ----- Performance by Edge Time Frame -----
    st.markdown("### 📊 Performance by Edge Time Frame")
    
    # Group by 'Edge Time Frame' and calculate average profit per time frame
    time_frame_performance = df.groupby('Edge Time Frame')['Profit'].mean().sort_values(ascending=False)
    st.write(time_frame_performance)
    
    # ----- Display Data Table -----
    st.markdown("### 📊 All Trades Data")
    st.dataframe(df)
  
