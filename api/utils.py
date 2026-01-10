from spotipy.oauth2 import SpotifyOAuth #Authenticates the USER
import spotipy
import os

def get_spotify_oauth(redirect_uri: str) -> SpotifyOAuth:
    """
    Centralizes the configuration so you don't repeat Client ID/Secret everywhere.
    Accepts the dynamic redirect_uri as an argument.
    """
    return SpotifyOAuth(
        client_id=os.environ.get("SPOTIPY_CLIENT_ID"),
        client_secret=os.environ.get("SPOTIPY_CLIENT_SECRET"),
        scope='user-read-private playlist-modify-public',
        redirect_uri=redirect_uri
        # in production, might also want to set open_browser=False
        # and cache_handler=... to prevent writing .cache files to disk
    )

def extract_message(raw_content: str | list) -> str:
    if isinstance(raw_content, list):
        #join blocks that are of type "text"
        ai_message = "".join(
            block.get("text", "")
            for block in raw_content
            if isinstance(block, dict) and block.get("type") == "text"
        )
        return ai_message
    else:
        return str(raw_content)