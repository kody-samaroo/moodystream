# moodystream/mood_engine/mood_classifier.py

from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from app.auth.spotify_auth import get_spotify_oauth, get_token_from_code
from app.utilts.mood_rules import classify_mood  # assuming you created this already

def get_mood_data(token):
    sp = Spotify(auth=token)

    # Step 1: Get user's top tracks
    top_tracks = sp.current_user_top_tracks(limit=20, time_range='short_term')

    # Step 2: Extract track IDs
    track_ids = [track['id'] for track in top_tracks['items']]

    # Step 3: Get audio features
    audio_features = sp.audio_features(track_ids)

    # Step 4: Match each track to its mood
    mood_data = []
    for track, features in zip(top_tracks['items'], audio_features):
        mood_data.append({
            "name": track['name'],
            "artist": track['artists'][0]['name'],
            "mood": classify_mood(features)
        })

    return mood_data
