import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Multi-Account Tracker", layout="wide")

FILE = "tiktok_daily_stats.csv"

if os.path.exists(FILE):
    df = pd.read_csv(FILE)
    df['Date'] = pd.to_datetime(df['Date'])
    
    # SIDEBAR: Account Selector
    st.sidebar.title("Settings")
    available_users = df['Username'].unique()
    selected_user = st.sidebar.selectbox("Choose Account", available_users)
    
    # Filter data for selected user
    user_df = df[df['Username'] == selected_user].sort_values("Date")
    
    st.title(f"📊 Stats for @{selected_user}")

    if not user_df.empty:
        latest = user_df.iloc[-1]
        
        # Growth Calculation
        if len(user_df) > 1:
            prev = user_df.iloc[-2]
            f_delta = int(latest['Followers'] - prev['Followers'])
        else:
            f_delta = 0

        # Big Metrics
        col1, col2, col3 = st.columns(3)
        col1.metric("Followers", f"{int(latest['Followers']):,}", delta=f"{f_delta:,}" if f_delta != 0 else None)
        col2.metric("Total Likes", f"{int(latest['Likes']):,}")
        col3.metric("Videos", f"{int(latest['Videos']):,}")

        # Comparison Chart
        st.subheader("📈 Follower Growth")
        st.line_chart(user_df.set_index("Date")["Followers"])
        
        # History Table
        st.subheader("🗓️ Log History")
        st.dataframe(user_df.sort_values("Date", ascending=False), use_container_width=True)
else:
    st.title("TikTok Performance Tracker")
    st.info("Collecting initial data for your accounts. Please run the GitHub Action.")
