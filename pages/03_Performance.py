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
    
    # ----- Performance by Edge Time Frame, Ecole, and Edge -----
    st.markdown("### 📊 Performance by Edge Time Frame, Ecole, and Edge")
    
    # Group by 'Edge Time Frame', 'Ecole', and 'Edge' and calculate average profit
    performance_by_group = df.groupby(['Edge Time Frame', 'Ecole', 'Edge'])['Profit'].mean().reset_index()

    # Display the grouped performance
    st.write(performance_by_group)
    
    # ----- Performance Table -----
    st.markdown("### 📊 All Trades Data")
    st.dataframe(df)
    
    # ----- Download Button -----
    st.markdown("---")
    st.download_button("📥 Télécharger le rapport complet",
                       data=performance_by_group.to_csv(index=False),
                       file_name="performance_report.csv",
                       mime="text/csv")
    
else:
    st.error("Le fichier 'trades_annotes.csv' n'a pas été trouvé dans le répertoire '/Result/'.")
