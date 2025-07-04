import os
import requests
import webbrowser
import threading
from flask import Flask, request
from dotenv import load_dotenv
import boto3
import json

load_dotenv()

app = Flask(__name__)
tokens = {}

CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")
REDIRECT_URI = os.getenv("SPOTIPY_REDIRECT_URI")
SCOPE = os.getenv("SCOPE")


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

    return ("Redirecting to Spotify...")

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
    
def get_secrets():
    client = boto3.client("secretsmanager")
    response = client.get_secret_value(SecretId="moodystream/spotify")
    secret_dict = json.loads(response["SecretString"])
    return secret_dict

def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    
def run_app():
    app.run(port=8888)

if __name__ == "__main__":
    threading.Thread(target=run_app).start()
    webbrowser.open("http://127.0.0.1:8888/callback")