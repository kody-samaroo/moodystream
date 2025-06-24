from dotenv import load_dotenv
import os
from spotipy.oauth2 import SpotifyOAuth

load_dotenv()

sp_oauth = SpotifyOAuth(
    client_id=os.getenv("SPOTIPY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
    redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
    scope=os.getenv("SCOPE")
)

token_info = sp_oauth.get_access_token(as_dict=True)
print(token_info["access_token"])
