import json
import glob
import os

bronze_files = glob.glob("data/bronze/spotify_raw_*.json")

latest_file = max(bronze_files, key=os.path.getctime)
print(f"Loading data from: {latest_file}...\n")

with open(latest_file, "r", encoding="utf-8") as f:
    spotify_data = json.load(f)

print("Top-level keys found:")
print(spotify_data.keys())

print("\nEndpoints inside user_data:")
print(spotify_data["user_data"].keys())
