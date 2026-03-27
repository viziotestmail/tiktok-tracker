import requests
import pandas as pd
from datetime import datetime
import os
import json
import re
import time

# --- LIST YOUR 4 ACCOUNTS HERE ---
USERNAMES = ["khaby.lame", "chloe.xoxo95", "solveig.chloe", "charlidamelio"] 
CSV_FILE = "tiktok_daily_stats.csv"

def get_user_data(username):
    url = f"https://www.tiktok.com/@{username.replace('@', '')}"
    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=30)
        if response.status_code != 200:
            return None

        pattern = r'<script id="__UNIVERSAL_DATA_FOR_REHYDRATION__" type="application/json">(.*?)</script>'
        match = re.search(pattern, response.text)
        if not match: return None

        raw_data = json.loads(match.group(1))
        user_info = raw_data.get("__DEFAULT_SCOPE__", {}).get("webapp.user-detail", {}).get("userInfo", {}).get("stats", {})
        
        return {
            "Date": datetime.now().strftime("%Y-%m-%d"),
            "Username": username,
            "Followers": user_info.get("followerCount", 0),
            "Likes": user_info.get("heartCount", 0),
            "Videos": user_info.get("videoCount", 0),
            "Total_Views": user_info.get("diggCount", 0)
        }
    except:
        return None

def track_all():
    all_results = []
    for user in USERNAMES:
        print(f"Tracking {user}...")
        data = get_user_data(user)
        if data:
            all_results.append(data)
        time.sleep(5) # 5-second pause to stay "stealthy"

    if not all_results:
        print("No data collected.")
        return

    df_new = pd.DataFrame(all_results)
    
    if os.path.exists(CSV_FILE):
        df_existing = pd.read_csv(CSV_FILE)
        # Combine and remove duplicates based on Date + Username
        df_final = pd.concat([df_existing, df_new]).drop_duplicates(subset=['Date', 'Username'], keep='last')
        df_final.to_csv(CSV_FILE, index=False)
    else:
        df_new.to_csv(CSV_FILE, index=False)
    
    print(f"Done! Updated stats for {len(all_results)} accounts.")

if __name__ == "__main__":
    track_all()
