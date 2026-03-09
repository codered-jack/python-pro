import spotipy
import os

CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID", "ADD_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET", "ADD_CLIENT_SECRET")
REDIRECT_URI = os.getenv("SPOTIPY_REDIRECT_URI", "http://example.com")
ACCESS_TOKEN = os.getenv("SPOTIPY_ACCESS_TOKEN", "ADD_ACCESS_TOKEN")
REFRESH_TOKEN = os.getenv("SPOTIPY_REFRESH_TOKEN", "")
SCOPE = "playlist-modify-private"


def get_spotify_client():
    """Return authenticated Spotipy client.

    Example:
    spotify = get_spotify_client()
    user_id = spotify.current_user()["id"]
    """
    spotify_client = spotipy.client.Spotify(auth=ACCESS_TOKEN, requests_session=True)

    spotify_oauth = spotipy.oauth2.SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        scope=SCOPE,
        requests_session=True,
        cache_path="token.txt",
    )

    # Optional refresh flow when refresh token is provided.
    if REFRESH_TOKEN:
        spotify_oauth.refresh_access_token(REFRESH_TOKEN)

    return spotify_client


def find_song_uris(spotify_client, year_to_travel, songs):
    """Resolve Billboard songs to Spotify track URIs.

    Example:
    uris = find_song_uris(spotify, "2005-03-20", ["Numb", "Hey Ya!"])
    """
    playlist = []

    for song in songs:
        song_tracks = spotify_client.search(
            f"track: {song} year: {year_to_travel}",
            limit=1,
            type="track",
        )
        try:
            song_uri = song_tracks["tracks"]["items"][0]["uri"]
            playlist.append(song_uri)
        except IndexError:
            print(f"Song not found on Spotify: {song}")
            continue

    return playlist


def create_billboard_playlist(year_to_travel, songs):
    """Create private playlist and add resolved track URIs.

    Returns:
        str: Created playlist ID.
    """
    spotify_client = get_spotify_client()
    user_id = spotify_client.current_user()["id"]
    playlist_uris = find_song_uris(spotify_client, year_to_travel, songs)

    playlist_id = spotify_client.user_playlist_create(
        user=user_id,
        name=f"{year_to_travel} Billboard 100",
        public=False,
        description="Music memory lane",
    )["id"]

    if playlist_uris:
        spotify_client.playlist_add_items(playlist_id=playlist_id, items=playlist_uris)

    return playlist_id