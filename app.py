import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="TikTok Leaderboard", layout="wide")

FILE = "tiktok_daily_stats.csv"

if os.path.exists(FILE):
    df = pd.read_csv(FILE)
    df['Date'] = pd.to_datetime(df['Date'])
    
    # --- SIDEBAR SETTINGS ---
    st.sidebar.title("Navigation")
    view_mode = st.sidebar.radio("Select View", ["Leaderboard", "Single Account Detail"])
    
    all_users = df['Username'].unique()

    # --- VIEW 1: THE LEADERBOARD ---
    if view_mode == "Leaderboard":
        st.title("🏆 Account Leaderboard")
        
        # Get the most recent data for each user
        latest_data = df.sort_values('Date').groupby('Username').tail(1).copy()
        
        # Calculate Growth (comparing latest to second-latest)
        growth_list = []
        for user in all_users:
            user_history = df[df['Username'] == user].sort_values('Date')
            if len(user_history) > 1:
                change = user_history.iloc[-1]['Followers'] - user_history.iloc[-2]['Followers']
            else:
                change = 0
            growth_list.append({"Username": user, "24h Growth": change})
        
        growth_df = pd.DataFrame(growth_list)
        leaderboard = pd.merge(latest_data, growth_df, on="Username")
        
        # Visual Comparison
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Total Followers")
            st.bar_chart(leaderboard.set_index("Username")["Followers"])
        with col2:
            st.subheader("24h Growth (New Followers)")
            st.bar_chart(leaderboard.set_index("Username")["24h Growth"])

        # The Rankings Table
        st.subheader("Rankings Table")
        display_cols = ["Username", "Followers", "24h Growth", "Likes", "Videos"]
        st.dataframe(
            leaderboard[display_cols].sort_values("Followers", ascending=False), 
            use_container_width=True,
            hide_index=True
        )

    # --- VIEW 2: SINGLE ACCOUNT DETAIL ---
    else:
        selected_user = st.sidebar.selectbox("Choose Account", all_users)
        user_df = df[df['Username'] == selected_user].sort_values("Date")
        
        st.title(f"📊 Detail: @{selected_user}")
        latest = user_df.iloc[-1]
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Followers", f"{int(latest['Followers']):,}")
        col2.metric("Total Likes", f"{int(latest['Likes']):,}")
        col3.metric("Videos", f"{int(latest['Videos']):,}")

        st.line_chart(user_df.set_index("Date")["Followers"])

else:
    st.title("TikTok Tracker")
    st.info("No data found. Ensure your GitHub Action has run successfully.")
