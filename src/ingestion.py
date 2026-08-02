import spotipy
import os
import json
from datetime import datetime
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth

load_dotenv()

SCOPES = (
    "user-read-recently-played user-top-read user-library-read playlist-read-private"
)


def fetch_bronze_data():
    print("--- Starting Spotify Ingestion Pipeline ---")

    os.makedirs("data/bronze", exist_ok=True)

    try:
        sp = spotipy.Spotify(
            auth_manager=SpotifyOAuth(
                client_id=os.getenv("SPOTIPY_CLIENT_ID"),
                client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
                redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
                scope=SCOPES,
                open_browser=False,
            )
        )

        raw_payload = {
            "metadata": {
                "ingestion_timestamp": datetime.now().isoformat(),
                "source": "spotify_api",
            },
            "user_data": {},
        }

        print("Fetching recently played tracks...")
        recent = sp.current_user_recently_played(limit=50)
        raw_payload["user_data"]["recently_played"] = recent

        print("Fetching top artists...")
        top_artists = sp.current_user_top_artists(limit=50, time_range="short_term")
        raw_payload["user_data"]["top_artists_short_term"] = top_artists

        print("\n=============================================")
        print("  YOUR TOP 5 ARTISTS (LAST 4 WEEKS)")
        print("=============================================")
        if len(top_artists["items"]) > 0:
            for i, artist in enumerate(top_artists["items"][:5]):
                print(f"  {i+1}. {artist['name']}")
        else:
            print("  No top artists found (Brand new account?)")
        print("=============================================\n")

        print("Fetching top tracks...")
        top_tracks = sp.current_user_top_tracks(limit=50, time_range="short_term")
        raw_payload["user_data"]["top_tracks_short_term"] = top_tracks

        print("Fetching saved library tracks...")
        raw_payload["user_data"]["saved_tracks"] = sp.current_user_saved_tracks(
            limit=50
        )

        print("Fetching user playlists...")
        raw_payload["user_data"]["playlists"] = sp.current_user_playlists(limit=50)

        timestamp = int(datetime.now().timestamp())
        filename = f"data/bronze/spotify_raw_{timestamp}.json"

        with open(filename, "w", encoding="utf-8") as f:
            json.dump(raw_payload, f, indent=4)

        print(f"JSON saved to: {filename}")

    except Exception as e:
        print(f"\ERROR during ingestion: {e}")


if __name__ == "__main__":
    fetch_bronze_data()
