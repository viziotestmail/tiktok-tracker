import requests
import pandas as pd
from datetime import datetime
import os
import json
import re

USERNAME = "khaby.lame" # Change to yours
CSV_FILE = "tiktok_daily_stats.csv"

def track_stats():
    # We use the mobile URL as it's often less guarded
    url = f"https://www.tiktok.com/@{USERNAME.replace('@', '')}"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
    }
    
    try:
        print(f"Bypassing blocks for {USERNAME}...")
        response = requests.get(url, headers=headers, timeout=30)
        
        if response.status_code != 200:
            print(f"❌ Blocked by TikTok (Status {response.status_code}).")
            return

        # Use Regex to find the hidden JSON data in the page HTML
        # This is where TikTok hides the follower counts for the browser to read
        pattern = r'<script id="__UNIVERSAL_DATA_FOR_REHYDRATION__" type="application/json">(.*?)</script>'
        match = re.search(pattern, response.text)
        
        if not match:
            print("❌ Could not find data on page. Profile might be private or layout changed.")
            return

        raw_data = json.loads(match.group(1))
        # Deep dive into the JSON structure
        user_info = raw_data.get("__DEFAULT_SCOPE__", {}).get("webapp.user-detail", {}).get("userInfo", {}).get("stats", {})
        
        followers = user_info.get("followerCount", 0)
        likes = user_info.get("heartCount", 0)
        videos = user_info.get("videoCount", 0)
        views = user_info.get("diggCount", 0) # 'diggCount' is often used as a proxy for reach if views are hidden

        stats = {
            "Date": datetime.now().strftime("%Y-%m-%d"),
            "Followers": followers,
            "Likes": likes,
            "Videos": videos,
            "Total_Views": views
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
            
        print(f"🎉 Success! Logged {followers} followers and {likes} likes.")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    track_stats()
