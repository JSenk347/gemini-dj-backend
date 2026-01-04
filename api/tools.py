# this file defines the tools that the llm is able to use, such as searching for music
from langchain_core.tools import tool
import json
import spotipy
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth

load_dotenv()

scope = "playlist-modify-public" #determines type of access we have to a user's account

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

@tool
def search_spotify(query: str) -> json:
    """ 
    Searches Spotify for music based on the user's query and returns a list of track lists,
    where each track list contains three elements: track_name, artist_name, track_uri, img_url
    """ #comment required so that the LLM knows what the tool does

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

# # this code will be executed once the user clicks the "save playlist" button
# def save_playlist(user: str, name: str, track_uris: list) -> dict:
#     """Saves the created playlist to the user's profile"""
#     playlist = sp.user_playlist_create(user=user, name=name, public=True, collaborative=False, description="")
#     sp.playlist_add_items(playlist["id"], track_uris)

#     return playlist

# # this function will be executed once the user clicks the "add track" button
# def add_tracks(playlist: dict, track_uri: list):
#     """
#     Adds a track to a playlist
    
#     :param playlist: The playlist to add the tracks to.
#     :type playlist: dict
#     :param track_uri: URI of the track to be added to the playlist.
#     :type track_uri: list
#     """
#     sp.playlist_add_items(playlist["id"], track_uri)
    
# results = search_spotify("rock")
# print(results)

