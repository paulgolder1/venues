import unittest
from unittest.mock import patch, MagicMock
import get_genre_for_artist_from_spotify as spotify

class TestSpotifyFunctions(unittest.TestCase):

    @patch('get_genre_for_artist_from_spotify.requests.post')
    def test_get_spotify_access_token_success(self, mock_post):
        # Mock the response to simulate a successful token retrieval
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'access_token': 'test_token'}
        mock_post.return_value = mock_response

        token = spotify.get_spotify_access_token('test_client_id', 'test_client_secret')
        self.assertEqual(token, 'test_token')

    @patch('get_genre_for_artist_from_spotify.requests.post')
    def test_get_spotify_access_token_failure(self, mock_post):
        # Mock the response to simulate a failed token retrieval
        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_post.return_value = mock_response

        token = spotify.get_spotify_access_token('test_client_id', 'test_client_secret')
        self.assertIsNone(token)

    @patch('get_genre_for_artist_from_spotify.requests.get')
    def test_get_artist_genres_success(self, mock_get):
        # Mock the response to simulate a successful artist lookup
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'artists': {
                'items': [{
                    'name': 'Test Artist',
                    'genres': ['rock', 'pop']
                }]
            }
        }
        mock_get.return_value = mock_response

        genres = spotify.get_artist_genres('Test Artist', 'test_token')
        self.assertEqual(genres, ['rock', 'pop'])

    @patch('get_genre_for_artist_from_spotify.requests.get')
    def test_get_artist_genres_no_artist(self, mock_get):
        # Mock the response to simulate no artist found
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'artists': {
                'items': []
            }
        }
        mock_get.return_value = mock_response

        genres = spotify.get_artist_genres('Nonexistent Artist', 'test_token')
        self.assertEqual(genres, [])

    def test_get_unique_artists_from_csv(self):
        # Create a mock CSV file content
        csv_content = [
            ["Show Name", "Artist Name"],
            ["Show 1", "Artist 1"],
            ["Show 2", "Artist 2"],
            ["Show 3", "Artist 1"]  # Duplicate artist
        ]
        
        # Mock the open function to return the CSV content
        with patch('builtins.open', unittest.mock.mock_open(read_data='\n'.join([','.join(row) for row in csv_content]))):
            artists = spotify.get_unique_artists_from_csv('mock_shows.csv')
            self.assertEqual(sorted(artists), sorted(['Artist 1', 'Artist 2']))

    @patch('get_genre_for_artist_from_spotify.csv.writer')
    def test_save_genres_to_csv(self, mock_writer):
        # Mock the CSV writer
        mock_csvfile = MagicMock()
        mock_writer.return_value = unittest.mock.MagicMock()

        artist_genres = [
            ('Artist 1', ['rock', 'pop']),
            ('Artist 2', ['jazz'])
        ]
        
        spotify.save_genres_to_csv(artist_genres, 'mock_artist_genres.csv')
        
        # Check if writerow was called with the correct arguments
        mock_writer.return_value.writerow.assert_any_call(["Artist Name", "Genre"])
        mock_writer.return_value.writerow.assert_any_call(['Artist 1', 'rock'])
        mock_writer.return_value.writerow.assert_any_call(['Artist 1', 'pop'])
        mock_writer.return_value.writerow.assert_any_call(['Artist 2', 'jazz'])

if __name__ == '__main__':
    unittest.main()