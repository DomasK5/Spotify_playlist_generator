from SpotifyAuth import SpotifyAuth
from Playlist import Playlist
from SearchTracksByGenre import SearchTracksByGenre
from SearchTracksByActivity import SearchTracksByActivity
import json
from requests import post


class SpotifyPlaylistGenerator:
    """Main class for generating playlists using different strategies"""

    def __init__(self):
        self.auth = SpotifyAuth()
        self.playlist = Playlist()
        self.search_strategy = None

    def set_strategy(self, strategy_type):
        """Set the search strategy"""
        if strategy_type == "genre":
            self.search_strategy = SearchTracksByGenre(self.auth)
        elif strategy_type == "activity":
            self.search_strategy = SearchTracksByActivity(self.auth)
        else:
            raise ValueError(f"Unknown strategy type: {strategy_type}")

    def generate_playlist(self, query, num_tracks=20, playlist_name=None):
        """Generate a playlist using the current strategy"""
        if not self.search_strategy:
            raise ValueError("Search strategy not set")

        if playlist_name:
            self.playlist.name = playlist_name

        self.playlist = Playlist(name=self.playlist.name)

        tracks = self.search_strategy.search_tracks(query, num_tracks)

        self.playlist.add_tracks(tracks)

        return self.playlist

    def create_spotify_playlist(self, user_id, access_token):
        """Create the playlist in the user's Spotify account"""
        if not self.playlist.tracks:
            print("No tracks in playlist")
            return None

        create_url = f"https://api.spotify.com/v1/users/{user_id}/playlists"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }

        data = {
            "name": self.playlist.name,
            "description": self.playlist.description,
            "public": True
        }

        response = post(create_url, headers=headers, data=json.dumps(data))
        playlist_data = json.loads(response.content)

        if "id" not in playlist_data:
            print(f"Error creating playlist: {playlist_data}")
            return None

        playlist_id = playlist_data["id"]

        tracks_url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
        track_uris = self.playlist.get_track_uris()

        for i in range(0, len(track_uris), 100):
            batch = track_uris[i:i+100]
            data = {"uris": batch}
            post(tracks_url, headers=headers, data=json.dumps(data))

        return playlist_id
