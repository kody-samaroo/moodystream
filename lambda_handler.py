import os
import json
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from mangum import Mangum
from starlette.middleware.wsgi import WSGIMiddleware
from server import app

asgi_app = WSGIMiddleware(app)
handler = Mangum(asgi_app)

def lambda_handler(event, context):
    return handler(event, context)

    # Load credentials and create Spotify client
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=os.getenv("SPOTIPY_CLIENT_ID"),
        client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
        redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
        scope=os.getenv("SCOPE")
    ))

    # Get current user ID
    user_id = sp.current_user()["id"]

    # Get top artists and create playlists
    artists = get_top_artists(sp, limit=3)
    playlist_ids = create_genre_playlists_from_top_artists(sp, user_id, artists)

    # Return JSON response
    return {
        'statusCode': 200,
        'body': json.dumps({
            "message": "Playlists created",
            "playlist_ids": playlist_ids
        })
    }


# Helper function: Get top artists
def get_top_artists(sp, limit=3, time_range='short_term'):
    results = sp.current_user_top_artists(limit=limit, time_range=time_range)
    return [artist for artist in results['items'] if artist['genres']]


# Helper function: Create playlists from top artists' genres
def create_genre_playlists_from_top_artists(sp, user_id, artists):
    playlist_ids = []

    for artist in artists:
        if artist['genres']:
            genre = artist['genres'][0]
            track_uris = search_tracks_by_genre(sp, genre=genre, limit=20)
            if track_uris:
                playlist_id = create_genre_playlist(sp, user_id, genre, track_uris)
                playlist_ids.append(playlist_id)

    return playlist_ids


# Helper function: Search tracks by genre (using search)
def search_tracks_by_genre(sp, genre, limit=10):
    # For better results, consider using sp.recommendations() instead
    query = f'genre:"{genre}"'
    results = sp.search(q=query, limit=limit, type='track')
    return [track['uri'] for track in results['tracks']['items']]


# Helper function: Create a playlist and add tracks
def create_genre_playlist(sp, user_id, genre, track_uris):
    playlist_title = f"Your Vibe: {genre.title()}"
    playlist = sp.user_playlist_create(
        user=user_id,
        name=playlist_title,
        public=True,
        description="Generated from your top artists' genres"
    )
    sp.playlist_add_items(playlist_id=playlist["id"], items=track_uris)
    return playlist["id"]
