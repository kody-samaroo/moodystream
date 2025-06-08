# moodystream/auth/spotify_auth.py

import os
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth

load_dotenv()  # Load .env variables

print("Client ID:", os.getenv("SPOTIFY_CLIENT_ID"))
print("Secret:", os.getenv("SPOTIFY_CLIENT_SECRET"))

def get_spotify_oauth():
    return SpotifyOAuth(
        client_id=os.getenv("SPOTIFY_CLIENT_ID"),
        client_secret=os.getenv("SPOTIFY_CLIENT_SECRET"),
        redirect_uri=os.getenv("SPOTIFY_REDIRECT_URI"),
        scope="user-top-read user-read-recently-played playlist-modify-private"
    )

def get_auth_url():
    sp_oauth = get_spotify_oauth()
    return sp_oauth.get_authorize_url()

def get_token_from_code(auth_code):
    sp_oauth = get_spotify_oauth()
    return sp_oauth.get_access_token(auth_code)
