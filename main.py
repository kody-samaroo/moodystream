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


# Fetch's the current user's top tracks
# top_tracks = get_top_tracks()
def get_top_tracks(limit=5, time_range='short_term'):
    results = sp.current_user_top_tracks(limit=limit, time_range=time_range)
    tracks = results['items']
    print(f"\n Your Top {limit} Tracks:\n")
    for i, track in enumerate(tracks):
        print(f"{i + 1}. {track['name']} — {track['artists'][0]['name']}")
    return tracks


# Fetch the current user's top artists
# top_artists = get_top_artists()
def get_top_artists(limit=10, time_range='short_term'):
    results = sp.current_user_top_artists(limit=limit, time_range=time_range)
    artists = []
    
    print("\n Top Artists and Their Genres:\n")
    for i, artist in enumerate(results['items']):
        if artist['genres']:  # Only include artists with at least 1 genre
            artists.append(artist)
            print(f"{1 + artists.index(artist)}. {artist['name']} — Genres: {', '.join(artist['genres'])}")

    return artists[:3] 

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


# TESTING search_tracks_by_genre() function
# artists = get_top_artists()

# for artist in artists:
#     genre = artist['genres'][0]
#     tracks = search_tracks_by_genre(genre)

def create_genre_playlist(user_id, genre, track_uris):
    playlist_title = f"Your Vibe: {genre}"
    playlist = sp.user_playlist_create(
        user=user_id, 
        name=playlist_title.capitalize(), 
        public=True, 
        description="Generated from your top artists' genres"
    )
    playlist_id = playlist["id"]
    sp.playlist_add_items(playlist_id=playlist_id, items=track_uris)

    return playlist_id

# TESTING create_genre_playlist() function
# user_id = sp.current_user()["id"]
# print(f"User ID: {user_id}")

# genre = "Rap"
# sample_tracks = [
# "spotify:track:6PGoSes0D9eUDeeAafB2As",
# "spotify:track:4iZ4pt7kvcaH6Yo8UoZ4s2",
# "spotify:track:6LxSe8YmdPxy095Ux6znaQ"
# ]

# create_genre_playlist(user_id, genre, sample_tracks)

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
    # 1. Initialize an empty list to store playlist IDs
    # 2. For each artist in the list of top artists:
        # a. Get the list of genres for that artist
        # b. If the artist has no genres, skip them
        # c. Use only the first genre (for simplicity)
        # d. Search for tracks using your `search_tracks_by_genre` function
        # e. If there are tracks, create a playlist using `create_genre_playlist`
        # f. Append the playlist ID to your list

    # 3. Return the list of created playlist IDs
