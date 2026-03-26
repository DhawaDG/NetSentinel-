
import streamlit as st
import sqlite3
import pandas as pd
from streamlit_option_menu import option_menu # Optional: pip install streamlit-option-menu

st.set_page_config(page_title="IT Ops Dashboard", layout="wide")

# Sidebar Menu
with st.sidebar:
    selected = option_menu(
        menu_title="Main Menu",
        options=["Live Dashboard", "Database History", "System Settings"],
        icons=["activity", "database", "gear"],
        menu_icon="cast",
        default_index=0,
    )

def get_data():
    conn = sqlite3.connect('database.db')
    df = pd.read_sql_query("SELECT * FROM device_logs ORDER BY timestamp DESC", conn)
    conn.close()
    return df

if selected == "Live Dashboard":
    st.title("🌐 Live IT Infrastructure Status")
    df = get_data()
    
    if not df.empty:
        # Get only the latest session
        latest_session = df[df['session_id'] == df['session_id'].iloc[0]]
        
        # Metrics
        col1, col2, col3 = st.columns(3)
        total = len(latest_session)
        online = len(latest_session[latest_session['status'] == 'Online'])
        offline = total - online
        
        col1.metric("Total Devices", total)
        col2.metric("Online", online, delta_color="normal")
        col3.metric("Critical Offline", offline, delta="-"+str(offline) if offline > 0 else "0", delta_color="inverse")

        st.table(latest_session[['device_name', 'status', 'timestamp']])
    else:
        st.warning("No logs found. Run extract.py to begin.")

if selected == "Database History":
    st.title("📅 Historical Logs by Day")
    df = get_data()
    
    df['date'] = pd.to_datetime(df['timestamp']).dt.date
    available_dates = df['date'].unique()
    date_choice = st.selectbox("Select Date", available_dates)
    
    filtered_df = df[df['date'] == date_choice]
    st.dataframe(filtered_df, use_container_width=True)




#pip install pandas streamlit streamlit-option-menu