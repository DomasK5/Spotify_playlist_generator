import unittest
from unittest.mock import Mock, patch
from SearchTracksByGenre import SearchTracksByGenre
from Track import Track


class TestSearchTracksByGenre(unittest.TestCase):
    def setUp(self):
        self.mock_auth = Mock()
        self.searcher = SearchTracksByGenre(self.mock_auth)

    def test_search_tracks_empty_result(self):
        """Test searching with no results"""
        self.searcher._search_tracks_by_genre = Mock(return_value=[])
        result = self.searcher.search_tracks("nonexistent_genre", 10)
        self.assertEqual(len(result), 0)

    def test_search_tracks_exact_amount(self):
        """Test searching with exact number of tracks needed"""
        mock_tracks = [
            Track({"id": str(i), "name": f"Track {i}"})
            for i in range(10)
        ]
        self.searcher._search_tracks_by_genre = Mock(return_value=mock_tracks)

        result = self.searcher.search_tracks("rock", 10)
        self.assertEqual(len(result), 10)

    def test_search_tracks_duplicate_filtering(self):
        """Test that duplicate tracks are filtered out"""
        # Create tracks with same signature
        duplicate_tracks = [
            Track({"id": "1", "name": "Same Track"}),
            Track({"id": "1", "name": "Same Track"})
        ]
        self.searcher._search_tracks_by_genre = Mock(return_value=duplicate_tracks)

        result = self.searcher.search_tracks("rock", 2)
        self.assertEqual(len(result), 1)


if __name__ == '__main__':
    unittest.main()
