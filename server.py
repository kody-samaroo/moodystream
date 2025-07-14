import boto3
import os
import requests
import webbrowser
import threading
from flask import Flask, request, redirect
import json
import spotipy

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

    print("🔗 Redirect URI being sent:", REDIRECT_URI)

    webbrowser.open(auth_url)

    return redirect(auth_url)

@app.route("/callback")
def callback():
    code = request.args.get("code")

    print("🔁 Query string:", request.query_string)
    print("🔍 All args:", request.args)


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
        print("✅ Access Token:", access_token)

        # 🎧 Step 2: Use Spotipy to access user's profile
        sp = spotipy.Spotify(auth=access_token)
        user_id = sp.current_user()["id"]
        print("👤 User ID:", user_id)

        # 🛠️ Step 3: Create a playlist
        sp.user_playlist_create(user=user_id, name="Lambda Test", public=True)
        print("🎉 Playlist created successfully!")

        print("Access Token:", tokens["access_token"])
        print("Refresh Token:", tokens["refresh_token"])

    else:
        return f"Token exchange failed. Response: {token_data}"

    shutdown_server()
    return "Authorization complete! You can close this tab."

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