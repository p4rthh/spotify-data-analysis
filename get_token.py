import os
import json
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth

load_dotenv()

client_id = os.getenv("SPOTIPY_CLIENT_ID")
client_secret = os.getenv("SPOTIPY_CLIENT_SECRET")
redirect_uri = os.getenv("SPOTIPY_REDIRECT_URI")

print(f"Using Client ID: {client_id[:5]}...")
print(f"Using Redirect URI: {redirect_uri}")

sp_oauth = SpotifyOAuth(
    client_id=client_id,
    client_secret=client_secret,
    redirect_uri=redirect_uri,
    scope="user-read-recently-played user-top-read",
    open_browser=False,
)

auth_url = sp_oauth.get_authorize_url()

print("\n================ STEP 1 ================")
print("Copy this link and open it in your browser:")
print(auth_url)
print("========================================\n")

response_url = input("Paste the FULL redirected URL from your address bar here:\n> ")

try:
    code = sp_oauth.parse_response_code(response_url)
    token_info = sp_oauth.get_access_token(code)

    # Explicitly write the token payload into .cache
    with open(".cache", "w", encoding="utf-8") as f:
        json.dump(token_info, f)

    print("\nSUCCESS! Token explicitly written to .cache file!")
except Exception as e:
    print(f"\nFailed to process token: {e}")
