from dotenv import load_dotenv
import os
import random
import spotipy
from spotipy.oauth2 import SpotifyOAuth

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
        artist_id = artist['id']
        tracks.append(get_artist_top_track(artist_id))
        tracks.append(get_artist_less_popular_track(artist_id))
        tracks.append(get_artist_less_popular_track(artist_id))

    playlist = create_playlist(user_id, tracks)

    print("\n Done! Created the following playlist:")
    print(f"https://open.spotify.com/playlist/{playlist['id']}")

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

    return tracks[0]['uri']

def get_artist_less_popular_track(artist_id):
    results = sp.artist_top_tracks(artist_id=artist_id, country='US')
    tracks = results['tracks']
    tracks.sort(key=lambda track: track['popularity'])

    int_random = random.randint(0, int(len(tracks)/2))

    return tracks[int_random]['uri']

def create_playlist(user, tracks):
    playlist = sp.user_playlist_create(user=user, name="A Personal Vibe", public=True, description="Playist made with an automated app. Thanks")
    sp.user_playlist_add_tracks(user=user, playlist_id=playlist['id'], tracks=tracks, position=None)

    return playlist

main()