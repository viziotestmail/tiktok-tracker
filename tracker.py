import requests
import pandas as pd
from datetime import datetime
import os

# --- SETTINGS ---
USERNAME = "khaby.lame"  # Change this to your username (no @ needed)
CSV_FILE = "tiktok_daily_stats.csv"
# We're using the Countik internal API
API_URL = f"https://countik.com/api/userinfo?user={USERNAME.replace('@', '')}"

def track_stats():
    # 1. Pretend to be a real browser to avoid being blocked
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    try:
        print(f"Attempting to fetch data for: {USERNAME}...")
        response = requests.get(API_URL, headers=headers, timeout=15)
        
        # Check if the website actually sent data back
        if response.status_code != 200:
            print(f"❌ API Error: Received status code {response.status_code}")
            print(f"Response text: {response.text[:200]}") # Show first 200 chars of error
            return

        data = response.json()
        
        # 2. Extract metrics (with '0' as a backup if a field is missing)
        followers = data.get("followerCount", 0)
        likes = data.get("heartCount", 0)
        videos = data.get("videoCount", 0)
        views = data.get("viewCount", 0) 
        
        # If all stats are 0, the user likely wasn't found
        if followers == 0 and likes == 0:
            print(f"⚠️ Warning: Received 0 for all stats. Is '{USERNAME}' a valid public profile?")
            return

        date_today = datetime.now().strftime("%Y-%m-%d")
        new_entry = pd.DataFrame([[date_today, followers, likes, videos, views]], 
                                columns=["Date", "Followers", "Likes", "Videos", "Total_Views"])
        
        # 3. Save the file
        if os.path.exists(CSV_FILE):
            df = pd.read_csv(CSV_FILE)
            if date_today in df['Date'].values:
                print(f"✅ Stats for {date_today} already recorded. Skipping save.")
                return
            new_entry.to_csv(CSV_FILE, mode='a', header=False, index=False)
        else:
            new_entry.to_csv(CSV_FILE, index=False)
            
        print(f"📊 Successfully logged: {followers} Followers | {likes} Likes")
        
    except Exception as e:
        print(f"❌ A Python error occurred: {str(e)}")

if __name__ == "__main__":
    track_stats()
