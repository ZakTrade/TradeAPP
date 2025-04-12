# 01_Another_trade.py
import pytz
from datetime import datetime

# ----- Strategy / Edge Mapping -----
edges_dict = {
    "ICT": ["FVG", "OTE", "BOS", "SMT", "Breaker", "Liquidity Sweep", "Judas Swing", "Autre"],
    "SMC": ["CHoCH", "BOS", "FVG", "Order Block", "Liquidity Grab", "Autre"],
    "Wyckoff": ["Spring", "Upthrust", "PSY", "AR", "ST", "LPS", "SOW", "Autre"],
    "Price Action": ["Pin Bar", "Engulfing", "Break & Retest", "Inside Bar", "Autre"],
    "Breakout": ["Breakout Range", "Retest", "Volume Spike", "Autre"],
    "Autre": ["Edge personnalisé"]
}

def get_session_from_time(trade_time, user_timezone):
    """Calculate the session based on local trade time"""
    local_tz = pytz.timezone(user_timezone)
    # Localize the trade time based on the user's selected timezone
    trade_time_local = local_tz.localize(trade_time)

    # Check the session based on the local time
    if 0 <= trade_time_local.hour < 8:
        return "Asia"
    elif 8 <= trade_time_local.hour < 13:
        return "London"
    elif 13 <= trade_time_local.hour < 22:
        return "New York"
    else:
        return "After Hours"

def process_trade_data(df, timezone):
    """
    Process the trade data and calculate session based on Open Time and user's selected timezone.
    This function is called in the app.py to update the dataframe with the 'Session' column.
    """
    df['Session'] = ""
    for i in range(len(df)):
        open_time_str = df.at[i, "Open Time"]
        try:
            trade_time = pd.to_datetime(open_time_str, format='%Y.%m.%d %H:%M:%S', errors='coerce')  # Custom format
            if pd.isnull(trade_time):
                raise ValueError(f"Le format de `Open Time` est incorrect pour le trade #{i + 1}.")
            
            session = get_session_from_time(trade_time, timezone)
            df.at[i, 'Session'] = session
        except Exception as e:
            df.at[i, 'Session'] = "Inconnu"
            print(f"Error processing trade #{i + 1}: {e}")
    return df
