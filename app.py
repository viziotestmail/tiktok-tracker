import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="TikTok Viral Tracker", layout="wide")

FILE = "tiktok_daily_stats.csv"

if os.path.exists(FILE):
    df = pd.read_csv(FILE)
    df['Date'] = pd.to_datetime(df['Date'])
    
    st.sidebar.title("Navigation")
    view_mode = st.sidebar.radio("Select View", ["Leaderboard", "Single Account Detail"])
    all_users = df['Username'].unique()

    if view_mode == "Leaderboard":
        st.title("🏆 Viral Leaderboard")
        
        # 1. Calculate Stats & Percentage Growth
        latest_stats = []
        for user in all_users:
            user_history = df[df['Username'] == user].sort_values('Date')
            if len(user_history) >= 1:
                latest = user_history.iloc[-1]
                
                # Default growth values
                abs_growth = 0
                pct_growth = 0.0
                
                if len(user_history) > 1:
                    prev = user_history.iloc[-2]
                    abs_growth = latest['Followers'] - prev['Followers']
                    # Avoid division by zero
                    if prev['Followers'] > 0:
                        pct_growth = (abs_growth / prev['Followers']) * 100
                
                latest_stats.append({
                    "Username": user,
                    "Followers": latest['Followers'],
                    "24h Gain": abs_growth,
                    "Growth %": round(pct_growth, 2),
                    "Total Likes": latest['Likes'],
                    "Videos": latest['Videos']
                })
        
        leaderboard = pd.DataFrame(latest_stats).sort_values("Followers", ascending=False)

        # 2. Top-Level Comparison Charts
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Total Follower Count")
            st.bar_chart(leaderboard.set_index("Username")["Followers"])
        with col2:
            st.subheader("Daily Growth Rate (%)")
            # This shows who is actually "Trending"
            st.bar_chart(leaderboard.set_index("Username")["Growth %"])

        # 3. The Interactive Table
        st.subheader("Full Performance Rankings")
        
        # Styling the dataframe to highlight high growth
        def color_growth(val):
            color = 'green' if val > 0 else 'white'
            return f'color: {color}'

        styled_df = leaderboard.style.applymap(color_growth, subset=['Growth %', '24h Gain']) \
                                    .format({"Growth %": "{:.2f}%", "Followers": "{:,}", "24h Gain": "+{:,}"})

        st.dataframe(styled_df, use_container_width=True, hide_index=True)

    else:
        # --- SINGLE ACCOUNT DETAIL ---
        selected_user = st.sidebar.selectbox("Choose Account", all_users)
        user_df = df[df['Username'] == selected_user].sort_values("Date")
        
        st.title(f"📊 Detail: @{selected_user}")
        if not user_df.empty:
            latest = user_df.iloc[-1]
            
            # Show big metrics
            c1, c2, c3 = st.columns(3)
            c1.metric("Followers", f"{int(latest['Followers']):,}")
            c2.metric("Total Likes", f"{int(latest['Likes']):,}")
            c3.metric("Videos", f"{int(latest['Videos']):,}")

            st.subheader("Follower Trend")
            st.line_chart(user_df.set_index("Date")["Followers"])

else:
    st.title("TikTok Tracker")
    st.info("No data found. Ensure your GitHub Action has run successfully.")
