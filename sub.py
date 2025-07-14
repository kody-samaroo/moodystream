import spotipy
import os
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

load_dotenv()

# Authenticate
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id = os.getenv("SPOTIPY_CLIENT_ID"),
    client_secret = os.getenv("SPOTIPY_CLIENT_SECRET"),
    redirect_uri = os.getenv("SPOTIPY_REDIRECT_URI"),
    scope = os.getenv("SCOPE")
))

def main():
    user_id = sp.current_user()["id"]
    artists = get_top_artists()
    tracks = []

    for i, artist in enumerate(artists):
        artist_id = artist[i]['id']
        tracks.append(get_artist_top_track(artist_id))
        tracks.append(get_less_popular_track(artist_id))

    playlist = create_playlist(user_id)

    playlist_ids = create_genre_playlists_from_top_artists(user_id, artists)
    
    # print("\n Done! Created the following playlists:")

# HELPER FUNCTIONS
def get_top_artists(limit=8, time_range='medium_term'):
    results = sp.current_user_top_artists(limit=limit, time_range=time_range)
    artists = []
    for i, artist in enumerate(results['items']):
        if artist['name']:
            artists.append(artist)

    return artists[:8]

def get_artist_top_track(artist_id):
    results = sp.artist_top_tracks(artist_id=artist_id, country='US')
    tracks = results['tracks']
    tracks.sort(reverse=True, key=lambda track: track['popularity'])

    return tracks[0]

def get_less_popular_track(artist_id):
    results = sp.artist_top_tracks(artist_id=artist_id, country='US')
    tracks = results['tracks']
    tracks.sort(key=lambda track: track['popularity'])

    return tracks[0]

def create_playlist(user):
    sp.user_playlist_create(user=user, name="You Personal Vibe", public=True, description="Playist made with an automated app. Thanks")
    