import boto3
import json
import requests
import threading
import webbrowser
import spotipy
from flask import Flask, request, redirect

app = Flask(__name__)
tokens = {}

# Fetches Client ID and secret from AWS Secrets Manager
def get_secrets():
    client = boto3.client("secretsmanager")
    response = client.get_secret_value(SecretId="moodystream/spotify")
    secret_dict = json.loads(response["SecretString"])
    return secret_dict

secrets = get_secrets()

# AWS secrets
CLIENT_ID = secrets["SPOTIPY_CLIENT_ID"]
CLIENT_SECRET = secrets["SPOTIPY_CLIENT_SECRET"]
REDIRECT_URI = secrets["SPOTIPY_REDIRECT_URI"]
SCOPE = "user-top-read playlist-modify-public"


@app.route("/login")
def login():

    auth_url = (
    "https://accounts.spotify.com/authorize"
    f"?client_id={CLIENT_ID}"
    "&response_type=code"
    f"&redirect_uri={REDIRECT_URI}"
    f"&scope={SCOPE}"
    )

    print("Redirect URI being sent:", REDIRECT_URI)

    webbrowser.open(auth_url)

    return redirect(auth_url)

@app.route("/callback")
def callback():
    code = request.args.get("code")

    if not code:
        return "Authorization failed: No code received"

    payload = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET
    }

    response = requests.post("https://accounts.spotify.com/api/token", data=payload)
    token_data = response.json()

    if "access_token" in token_data:
        tokens["access_token"] = token_data["access_token"]
        tokens["refresh_token"] = token_data["refresh_token"]

        access_token = tokens["access_token"]

        sp = spotipy.Spotify(auth=access_token)
        user_id = sp.current_user()["id"]
        artists = get_top_artists(sp)
        tracks = []

        for i, artist in enumerate(artists):
            artist_id = artist['id']
            tracks.append(get_artist_top_track(sp, artist_id))
            tracks.append(get_artist_less_popular_track(sp, artist_id))

        playlist = create_playlist(sp, user_id, tracks)

        print("\n Done! Created the following playlist:")
        print(f"https://open.spotify.com/playlist/{playlist['id']}")

    else:
        return f"Token exchange failed. Response: {token_data}"

    shutdown_server()
    return "Authorization complete!"

def get_token():
    if "access_token" in tokens:
        return tokens["access_token"]
    else:
        print(f"Missing access token in the tokens dictionary.")
        return None

def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    
def run_app():
    app.run(port=8888)

if __name__ == "__main__":
    threading.Thread(target=run_app).start()
    webbrowser.open(REDIRECT_URI)


# HELPER FUNCTIONS
def get_top_artists(sp, limit=8, time_range='medium_term'):
    results = sp.current_user_top_artists(limit=limit, time_range=time_range)
    artists = []
    for i, artist in enumerate(results['items']):
        if artist['name']:
            artists.append(artist)

    return artists[:8]

def get_artist_top_track(sp, artist_id):
    results = sp.artist_top_tracks(artist_id=artist_id, country='US')
    tracks = results['tracks']
    tracks.sort(reverse=True, key=lambda track: track['popularity'])

    return tracks[0]['uri']

def get_artist_less_popular_track(sp, artist_id):
    results = sp.artist_top_tracks(artist_id=artist_id, country='US')
    tracks = results['tracks']
    tracks.sort(key=lambda track: track['popularity'])

    return tracks[0]['uri']

def create_playlist(sp, user, tracks):
    playlist = sp.user_playlist_create(user=user, name="A Personal Vibe", public=True, description="Playist made with an automated app. Thanks")
    sp.user_playlist_add_tracks(user=user, playlist_id=playlist['id'], tracks=tracks, position=None)

    return playlist