import requests
import pandas as pd
from datetime import datetime
import os

USERNAME = "khaby.lame" # Change to your username
CSV_FILE = "tiktok_daily_stats.csv"
API_URL = f"https://countik.com/api/userinfo?user={USERNAME.replace('@', '')}"

def track_stats():
    # Enhanced headers to bypass "Bot Detection"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "application/json",
        "Referer": "https://countik.com/tiktok-follower-count",
        "Origin": "https://countik.com"
    }
    
    try:
        print(f"Connecting to API for {USERNAME}...")
        response = requests.get(API_URL, headers=headers, timeout=20)
        
        if response.status_code != 200:
            print(f"❌ API Blocked us (Status {response.status_code}).")
            # Create an empty file so the GitHub Action doesn't crash
            if not os.path.exists(CSV_FILE):
                pd.DataFrame(columns=["Date", "Followers", "Likes", "Videos", "Total_Views"]).to_csv(CSV_FILE, index=False)
            return

        data = response.json()
        
        # Check if we actually got data
        followers = data.get("followerCount", 0)
        if followers == 0:
            print("⚠️ API returned 0. The account might be private or the username is wrong.")
            return

        stats = {
            "Date": datetime.now().strftime("%Y-%m-%d"),
            "Followers": followers,
            "Likes": data.get("heartCount", 0),
            "Videos": data.get("videoCount", 0),
            "Total_Views": data.get("viewCount", 0)
        }

        df_new = pd.DataFrame([stats])
        
        if os.path.exists(CSV_FILE):
            df_existing = pd.read_csv(CSV_FILE)
            if stats["Date"] in df_existing['Date'].values:
                print("✅ Already logged today.")
                return
            df_new.to_csv(CSV_FILE, mode='a', header=False, index=False)
        else:
            df_new.to_csv(CSV_FILE, index=False)
            
        print(f"🎉 Success! Logged {followers} followers.")
        
    except Exception as e:
        print(f"❌ Critical Error: {e}")

if __name__ == "__main__":
    track_stats()
