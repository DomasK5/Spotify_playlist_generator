from Track import Track
import json
from abc import ABC, abstractmethod
from requests import get


class TrackSearcher(ABC):
    """Abstract base class for track searching strategies"""
    def __init__(self, auth):
        self.auth = auth

    @abstractmethod
    def search_tracks(self, query, num_tracks=20):
        """Abstract method to search for tracks based on query"""
        pass

    def _search_tracks_by_genre(self, genre, limit=20, offset=0):
        """Helper method to search tracks by genre"""
        url = "https://api.spotify.com/v1/search"
        headers = self.auth.get_auth_header()
        query = f"q=genre:{genre}&type=track&limit={limit}&offset={offset}"
        url += f"?{query}"

        result = get(url, headers=headers)
        json_result = json.loads(result.content)

        if "tracks" in json_result and "items" in json_result["tracks"]:
            return [Track(item) for item in json_result["tracks"]["items"]]
        else:
            print(f"Error: Could not retrieve tracks for genre '{genre}'.")
            print(f"Response: {json_result}")
            return []
