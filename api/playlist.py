from typing import List, Dict
import os
import spotipy
from spotipy import SpotifyClientCredentials

MAX_PLAYLIST_SIZE = 10

class PlaylistSession:
    def __init__(self):
        # Own the auth manager so its token cache is reused across calls,
        # but create a fresh spotipy.Spotify (new HTTP session) per search
        # to avoid stale keep-alive connections being reused after Spotify
        # closes them on the server side.
        self._auth_manager = SpotifyClientCredentials(
            client_id=os.environ.get("SPOTIPY_CLIENT_ID"),
            client_secret=os.environ.get("SPOTIPY_CLIENT_SECRET")
        )
        self.current_tracks: List[Dict] = []

    def _sp(self) -> spotipy.Spotify:
        return spotipy.Spotify(auth_manager=self._auth_manager)

    def _existing_uris(self):
        return {t["track_uri"] for t in self.current_tracks}

    def search_and_add(self, query: str, limit: int = 1):
        """Searches Spotify and adds the top result to the playlist."""
        if len(self.current_tracks) >= MAX_PLAYLIST_SIZE:
            return "Playlist is full (10 songs). No more tracks will be added."

        results = self._sp().search(q=query, limit=limit, type="track")
        items = results["tracks"]["items"]
        existing = self._existing_uris()

        added = []
        for item in items:
            if len(self.current_tracks) >= MAX_PLAYLIST_SIZE:
                break
            uri = item["uri"]
            if uri in existing:
                continue
            img_url = item["album"]["images"][0]["url"] if item["album"]["images"] else ""
            track = {
                "track_uri": uri,
                "track_name": item["name"],
                "artist_name": item["artists"][0]["name"],
                "img_url": img_url
            }
            self.current_tracks.append(track)
            existing.add(uri)
            added.append(f"{track['track_name']} by {track['artist_name']}")

        return f"Added: {', '.join(added)}" if added else "No new tracks added (duplicate or playlist full)."

    def get_playlist_state(self):
        """Returns the current list of songs."""
        if not self.current_tracks:
            return "The playlist is currently empty."
        lines = [f"{t['track_name']} - {t['artist_name']}" for t in self.current_tracks]
        return f"{len(self.current_tracks)}/10 songs:\n" + "\n".join(lines)
