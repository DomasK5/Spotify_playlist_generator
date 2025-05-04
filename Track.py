class Track:
    """Class representing a Spotify track"""

    def __init__(self, track_data):
        self.id = track_data.get('id')
        self.name = track_data.get('name')
        self.artists = [
            artist['name'] for artist in track_data.get('artists', [])
        ]
        self.main_artist = self.artists[0] if self.artists else "Unknown"
        self.uri = track_data.get('uri')
        self.album = track_data.get('album', {}).get('name', "Unknown Album")
        self.popularity = track_data.get('popularity', 0)

    def __str__(self):
        return f"{self.name} by {self.main_artist}"

    def __repr__(self):
        return self.__str__()

    def get_signature(self):
        """Return a unique signature for the track to avoid duplicates"""
        return (self.name, self.main_artist)
