from typing import List, Dict

class PlaylistSession:
    def __init__(self, sp_client):
        self.sp = sp_client
        self.current_tracks: List[Dict] = []

    def search_and_add(self, query: str, limit: int = 1):
        """Searches Spotify and adds the tops result to the playlist."""
        results = self.sp.search(q=query, limit=limit, type="track")
        items = results["tracks"]["items"]

        added = []
        for item in items:
            img_url = item["album"]["images"][0]["url"] if len(item["album"]["images"]) > 0 else ""
            track = {
                "track_uri": item["uri"],
                "track_name": item["name"],
                "artist_name": item["artists"][0]["name"],
                "img_url": img_url
            }
            self.current_tracks.append(track)
            added.append(f"{track['track_name']} by {track['artist_name']}")

        return f"Added: {', '.join(added)}"
    
    def get_playlist_state(self):
        """Returns the current list of songs."""
        if not self.current_tracks:
            return "The playlist is currently empty."
        return "\n".join([f"{t['name']} - {t['artist']}" for t in self.current_tracks])
