import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="TikTok Daily Tracker", layout="wide")
st.title("📊 TikTok Performance Tracker")

# THE KEY: This must match your tracker.py filename exactly
FILE = "tiktok_daily_stats.csv"

if os.path.exists(FILE):
    df = pd.read_csv(FILE)
    
    # Ensure Date is recognized correctly
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.sort_values("Date")
    
    latest = df.iloc[-1]
    
    # Calculate daily change if we have at least 2 days of data
    if len(df) > 1:
        prev = df.iloc[-2]
        f_delta = int(latest['Followers'] - prev['Followers'])
        l_delta = int(latest['Likes'] - prev['Likes'])
    else:
        f_delta = l_delta = 0

    # 1. Metric Cards
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Followers", f"{int(latest['Followers']):,}", delta=f"{f_delta:,}" if f_delta != 0 else None)
    col2.metric("Total Likes", f"{int(latest['Likes']):,}", delta=f"{l_delta:,}" if l_delta != 0 else None)
    col3.metric("Videos", f"{int(latest['Videos']):,}")
    col4.metric("Estimated Views", f"{int(latest['Total_Views']):,}")

    # 2. Growth Chart
    st.subheader("📈 Growth Over Time")
    chart_data = df.set_index("Date")[["Followers", "Likes"]]
    st.line_chart(chart_data)

    # 3. History Table
    st.subheader("🗓️ Daily History Log")
    st.dataframe(df.sort_values("Date", ascending=False), use_container_width=True)

else:
    st.error(f"File '{FILE}' not found. Please check your GitHub repository.")
