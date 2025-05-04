class Playlist:
    """Class representing a collection of tracks"""

    def __init__(
            self,
            name="My Playlist",
            description="Generated with Spotify Playlist Generator"
            ):
        self.name = name
        self.description = description
        self.tracks = []
        self.seen_tracks = set()

    def add_track(self, track):
        """Add a track to the playlist if it's not already there"""
        signature = track.get_signature()
        if signature not in self.seen_tracks:
            self.tracks.append(track)
            self.seen_tracks.add(signature)
            return True
        return False

    def add_tracks(self, tracks):
        """Add multiple tracks to the playlist, avoiding duplicates"""
        added_count = 0
        for track in tracks:
            if self.add_track(track):
                added_count += 1
        return added_count

    def clear(self):
        """Clear all tracks from the playlist"""
        self.tracks = []
        self.seen_tracks.clear()

    def get_track_uris(self):
        """Return list of Spotify URIs for all tracks in the playlist"""
        return [track.uri for track in self.tracks if track.uri]

    def __len__(self):
        return len(self.tracks)
