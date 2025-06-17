from dotenv import load_dotenv
import os
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


# Fetch top tracks
def get_top_tracks(limit=5, time_range='short_term'):
    results = sp.current_user_top_tracks(limit=limit, time_range=time_range)
    tracks = results['items']
    print(f"\n Your Top {limit} Tracks:\n")
    for i, track in enumerate(tracks):
        print(f"{i + 1}. {track['name']} — {track['artists'][0]['name']}")
    return tracks

# top_tracks = get_top_tracks()

# Fetch top artists
def get_top_artists(limit=10, time_range='short_term'):
    results = sp.current_user_top_artists(limit=limit, time_range=time_range)
    artists = []
    
    print("\n Top Artists and Their Genres:\n")
    for i, artist in enumerate(results['items']):
        if artist['genres']:  # Only include artists with at least 1 genre
            artists.append(artist)
            print(f"{1 + artists.index(artist)}. {artist['name']} — Genres: {', '.join(artist['genres'])}")

    return artists[:3] 

# top_artists = get_top_artists()

# Search tracks for a given genre
def search_tracks_by_genre(genre, limit=20):
    query = f'genre:"{genre}"gi'
    results = sp.search(q=query, limit=10, type='track')
    tracks = results['tracks']['items']
    track_uris = [track['uri'] for track in tracks]
    print(f"Found {len(track_uris)} tracks for genre: {genre}")
    for i, track_uri in enumerate(track_uris):
        print(track_uri)

    return track_uris

# tracks_by_genre = search_tracks_by_genre()

artists = get_top_artists()

for artist in artists:
    genre = artist['genres'][0]
    tracks = search_tracks_by_genre(genre)