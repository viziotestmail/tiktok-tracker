import streamlit as st
import pandas as pd

st.set_page_config(page_title="TikTok Daily Tracker", layout="wide")
st.title("📊 TikTok Performance Tracker")

try:
    df = pd.read_csv("stats_history.csv")
    latest = df.iloc[-1]

    # Display Top Metrics in 3 Columns
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Followers", f"{latest['Followers']:,}")
    col2.metric("Total Likes", f"{latest['Likes']:,}")
    col3.metric("Total Videos", f"{latest['Videos']:,}")

    # Visualizing growth
    st.subheader("Growth Trends")
    tab1, tab2 = st.tabs(["Followers & Likes", "Video Count"])
    
    with tab1:
        st.line_chart(df.set_index("Date")[["Followers", "Likes"]])
    with tab2:
        st.bar_chart(df.set_index("Date")["Videos"])

    st.subheader("Raw Data History")
    st.dataframe(df.sort_values("Date", ascending=False), use_container_width=True)

except Exception:
    st.info("No data yet. It will appear after the first daily run!")
