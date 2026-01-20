from typing import List, Dict

NUM_RECS = 3

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
    
    def add_recommendations(self, genre: str = None, mood: str = None):
        """Uses the last added track as a seed to find similar songs."""
        if not self.current_tracks:
            return "Error: Add a track first to get recommendations."
        
        seed_track_uri = self.current_tracks[-1]["track_uri"].split(":")[-1] #extracting the id of the song

        recs = self.sp.recommendations(seed_tracks=[seed_track_uri], limit=NUM_RECS)

        added = []
        for item in recs["tracks"]:
            img_url = item["album"]["images"][0]["url"] if len(item["album"]["images"]) > 0 else ""
            track = {
                "track_uri": item["uri"],
                "track_name": item["name"],
                "artist_name": item["artists"][0]["name"],
                "img_url": img_url
            }
            self.current_tracks.append(track)
            added.append(f"{track['track_name']} by {track['artist_name']}")

        return f"Found and added recommendations based on previous track: {', '.join(added)}"
    
    def get_playlist_state(self):
        """Returns the current list of songs."""
        if not self.current_tracks:
            return "The playlist is currently empty."
        return "\n".join([f"{t['name']} - {t['artist']}" for t in self.current_tracks])
