# this file defines the tools that the llm is able to use, such as searching for music
from langchain_core.tools import tool
import json
import spotipy
import os
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth #Authenticates the USER
from spotipy.oauth2 import SpotifyClientCredentials #Authenticatest the SERVER. All that's needed for search functionality.
from .playlist import PlaylistSession

load_dotenv()

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id=os.environ.get("SPOTIPY_CLIENT_ID"),
    client_secret=os.environ.get("SPOTIPY_CLIENT_SECRET")
))

playlist = PlaylistSession(sp_client=sp)

@tool
def search_spotify(query: str) -> json:
    """ 
    Searches Spotify for music based on the user's query and returns a list of track lists,
    where each track list contains three elements: track_name, artist_name, track_uri, img_url
    """ #comment required so that the LLM knows what the tool does

    # auth_manager setup for PUBLIC data, only requiring client_id and client_secret
    auth_manager = SpotifyClientCredentials(
        client_id=os.environ.get("SPOTIPY_CLIENT_ID"),
        client_secret=os.environ.get("SPOTIPY_CLIENT_SECRET")
    )

    sp = spotipy.Spotify(auth_manager=auth_manager)

    results = sp.search(q=query, limit=10, type=["track"]) #returns a dictionary

    cleaned_results = []

    tracks_list = results.get('tracks', {}).get('items', [])

    for item in tracks_list:
        track_name = item.get('name', 'Unknown Track')
        artists = item.get('artists', [])
        artist_name = artists[0]['name'] if artists else "Unknown Artist"
        track_uri = item.get('uri', '')
        album = item.get('album', {})
        imgs = album.get('images', [])
        img_url = imgs[0]['url'] if imgs else ""

        track_info = [track_name, artist_name, track_uri, img_url]
        cleaned_results.append(track_info)

    return json.dumps(cleaned_results) 

# v2.0 CODE
@tool
def add_song(query: str):
    """
    Useful for when you need to search for a particular song and add it to the playlist.
    Input should be a search query such as "80's rock" or "Laufey".
    """
    return playlist.search_and_add(query)

@tool
def add_similar_songs(genre: str = "", mood: str = ""):
    """
    Useful for when you want to add 3 more songs to the playlist that are similar to the
    song that was most recently added. You can also search for and add similar songs that have a 
    different genre or mood.
    """
    return playlist.add_recommendations(genre, mood)

@tool
def check_playlist_status():
    """
    Useful to check what songs are currently in the playlist to ensure you aren't repeating artists
    or songs with the same title. Always check this before finalizing.
    """
    return playlist.get_playlist_state()

