import unittest
from Track import Track


class TestTrack(unittest.TestCase):
    def setUp(self):
        """Set up test data before each test"""
        self.track_data = {
            "id": "test123",
            "name": "Test Song",
            "artists": [
                {"name": "Test Artist"},
                {"name": "Featured Artist"}
            ],
            "uri": "spotify:track:test123",
            "preview_url": "https://test.com/preview"
        }
        self.track = Track(self.track_data)

    def test_track_initialization(self):
        """Test track object creation with data"""
        self.assertEqual(self.track.id, "test123")
        self.assertEqual(self.track.name, "Test Song")
        self.assertEqual(self.track.uri, "spotify:track:test123")

    def test_track_initialization_missing_data(self):
        """Test track object creation with missing data"""
        minimal_data = {"id": "123"}
        track = Track(minimal_data)
        self.assertEqual(track.id, "123")
        self.assertIsNone(track.name)
        self.assertIsNone(track.uri)

    def test_track_str_representation(self):
        """Test string representation of track"""
        expected_str = "Test Song by Test Artist"
        self.assertEqual(str(self.track), expected_str)

    def test_track_str_no_artists(self):
        """Test string representation with no artists"""
        self.track_data["artists"] = []
        track = Track(self.track_data)
        expected_str = "Test Song by Unknown"
        self.assertEqual(str(track), expected_str)

    def test_get_signature(self):
        """Test track signature generation"""
        signature1 = self.track.get_signature()

        # Create new track with same data
        track2 = Track(self.track_data)
        signature2 = track2.get_signature()

        # Signatures should match for same data
        self.assertEqual(signature1, signature2)

        # Change track data
        self.track_data["name"] = "different_artist"
        track3 = Track(self.track_data)
        signature3 = track3.get_signature()

        # Signatures should differ for different data
        self.assertNotEqual(signature1, signature3)


if __name__ == '__main__':
    unittest.main()
