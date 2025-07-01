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

def main():
    user_id = sp.current_user()["id"]
    artists = get_top_artists(limit=5)
    playlist_ids = create_genre_playlists_from_top_artists(user_id, artists)
    
    print("\n Done! Created the following playlists:")
    for pid in playlist_ids:
        print(f"https://open.spotify.com/playlist/{pid}")

# Helper function
# Fetch the current user's top artists
def get_top_artists(limit=10, time_range='short_term'):
    results = sp.current_user_top_artists(limit=limit, time_range=time_range)
    artists = []
    
    print("\n Top Artists and Their Genres:\n")
    for i, artist in enumerate(results['items']):
        if artist['genres']:  # Only include artists with at least 1 genre
            artists.append(artist)

    return artists[:3] 

# Helper function
# Queries for a list of tracks based of genre
def search_tracks_by_genre(genre, limit=10):
    query = f'genre:"{genre}"'
    results = sp.search(q=query, limit=10, type='track')
    tracks = results['tracks']['items']
    track_uris = [track['uri'] for track in tracks]

    return track_uris

def create_genre_playlist(user_id, genre, track_uris):
    playlist_title = f"Your Vibe: {genre.capitalize()}"
    playlist = sp.user_playlist_create(
        user=user_id, 
        name=playlist_title, 
        public=True, 
        description="Generated from your top artists' genres"
    )
    playlist_id = playlist["id"]
    sp.playlist_add_items(playlist_id=playlist_id, items=track_uris)

    return playlist_id

def create_genre_playlists_from_top_artists(user_id, artists):
    playlist_ids = []
    
    for i, artist in enumerate(artists):
        if artist['genres']:  # Only include artists with at least 1 genre
            genre = artist['genres'][0]
            results = search_tracks_by_genre(genre=genre, limit=20)
        if results:
            playlist_id = create_genre_playlist(
                user_id=user_id, 
                genre=genre, 
                track_uris=results
            )
            playlist_ids.append(playlist_id)

    return playlist_ids

main()