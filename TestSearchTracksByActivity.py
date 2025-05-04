import unittest
from unittest.mock import Mock, patch
from SearchTracksByActivity import SearchTracksByActivity
from Track import Track
import json


class TestSearchTracksByActivity(unittest.TestCase):
    def setUp(self):
        """Set up test environment"""
        self.mock_auth = Mock()
        self.mock_auth.get_auth_header.return_value = {
            "Authorization": "Bearer test_token"
        }
        self.searcher = SearchTracksByActivity(self.mock_auth)

    def test_invalid_activity(self):
        """Test with invalid activity"""
        result = self.searcher.search_tracks("not_a_real_activity")
        self.assertEqual(len(result), 0)

    @patch('TrackSearcher.get')
    def test_valid_activity(self, mock_get):
        """Test with valid activity"""
        # Create mock response data
        response_data = {
            "tracks": {
                "items": [
                    {"id": "1", "name": "Test Track"}
                ]
            }
        }

        # Mock the HTTP response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = json.dumps(response_data).encode('utf-8')
        mock_response.json.return_value = response_data
        mock_get.return_value = mock_response

        # Test with "Gaming" activity
        result = self.searcher.search_tracks("Gaming", 2)

        # Check if we got any tracks
        self.assertTrue(len(result) > 0)
        # Check if returned track has correct data
        self.assertEqual(result[0].id, "1")
        self.assertEqual(result[0].name, "Test Track")


if __name__ == '__main__':
    unittest.main()
