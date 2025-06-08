# moodystream/auth/get_top_tracks.py

import os
from dotenv import load_dotenv
from spotipy import Spotify
from spotify_auth import get_spotify_oauth, get_token_from_code

load_dotenv()

def get_top_tracks(token):
    sp = Spotify(auth=token)
    results = sp.current_user_top_tracks(limit=5, time_range='short_term')

    for i, item in enumerate(results['items']):
        print(f"{i+1}: {item['name']} by {item['artists'][0]['name']}")

    return results['items']

if __name__ == "__main__":
    token_info = get_spotify_oauth().get_cached_token()

    if not token_info:
        print("No cached token found. Please re-authenticate first.")
    else:
        access_token = token_info['access_token']
        print("Fetching top tracks...\n")
        get_top_tracks(access_token)
