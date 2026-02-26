import requests
import pandas as pd
from datetime import datetime
import os

USERNAME = "khaby.lame" # Change to your target username
CSV_FILE = "tiktok_daily_stats.csv"
API_URL = f"https://countik.com/api/userinfo?user={USERNAME}"

def track_stats():
    try:
        response = requests.get(API_URL).json()
        
        # Extracting metrics
        followers = response.get("followerCount", 0)
        likes = response.get("heartCount", 0)
        videos = response.get("videoCount", 0)
        # Attempt to get total views (sometimes labeled as 'playCount' or 'viewCount')
        views = response.get("viewCount", 0) 
        
        date_today = datetime.now().strftime("%Y-%m-%d")

        new_entry = pd.DataFrame([[date_today, followers, likes, videos, views]], 
                                columns=["Date", "Followers", "Likes", "Videos", "Total_Views"])
        
        if os.path.exists(CSV_FILE):
            df = pd.read_csv(CSV_FILE)
            # Prevent duplicate entries for the same day
            if date_today in df['Date'].values:
                print(f"Stats for {date_today} already exist. Skipping.")
                return
            new_entry.to_csv(CSV_FILE, mode='a', header=False, index=False)
        else:
            new_entry.to_csv(CSV_FILE, index=False)
            
        print(f"Successfully logged stats for {date_today}")
        
    except Exception as e:
        print(f"Error fetching data: {e}")

if __name__ == "__main__":
    track_stats()
