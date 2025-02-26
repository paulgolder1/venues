import unittest
from unittest.mock import patch, MagicMock
import get_band_members_v2 as band

class TestGetBandMembers(unittest.TestCase):

    @patch('get_band_members_v2.requests.get')
    def test_get_band_members_success(self, mock_get):
        # Mock the response to simulate a successful band search
        mock_search_response = MagicMock()
        mock_search_response.status_code = 200
        mock_search_response.json.return_value = {
            'artists': [{'id': 'test_band_id', 'name': 'Test Band'}]
        }
        mock_get.side_effect = [mock_search_response, MagicMock()]

        # Mock the response to simulate a successful band details fetch
        mock_details_response = MagicMock()
        mock_details_response.status_code = 200
        mock_details_response.json.return_value = {
            'relations': [
                {'type': 'member of band', 'artist': {'name': 'Member 1'}},
                {'type': 'member of band', 'artist': {'name': 'Member 2'}}
            ]
        }
        mock_get.side_effect = [mock_search_response, mock_details_response]

        members = band.get_band_members('Test Band')
        self.assertEqual(members, ['Member 1', 'Member 2'])

    @patch('get_band_members_v2.requests.get')
    def test_get_band_members_no_results(self, mock_get):
        # Mock the response to simulate no results found
        mock_search_response = MagicMock()
        mock_search_response.status_code = 200
        mock_search_response.json.return_value = {'artists': []}
        mock_get.return_value = mock_search_response

        members = band.get_band_members('Nonexistent Band')
        self.assertEqual(members, [])

    @patch('get_band_members_v2.requests.get')
    def test_get_band_members_error(self, mock_get):
        # Mock the response to simulate an error
        mock_search_response = MagicMock()
        mock_search_response.status_code = 500
        mock_get.return_value = mock_search_response

        members = band.get_band_members('Error Band')
        self.assertEqual(members, [])

    def test_format_time_remaining(self):
        # Test various cases for format_time_remaining
        self.assertEqual(band.format_time_remaining(45), '45 seconds')
        self.assertEqual(band.format_time_remaining(75), '1 minutes 15 seconds')
        self.assertEqual(band.format_time_remaining(120), '2 minutes')
        self.assertEqual(band.format_time_remaining(3600), '60 minutes')

    @patch('get_band_members_v2.get_band_members', return_value=['Member 1', 'Member 2'])
    @patch('get_band_members_v2.time.sleep', return_value=None)  # Skip sleep for testing
    @patch('get_band_members_v2.csv.writer')
    def test_process_artist_file(self, mock_writer, mock_sleep, mock_get_band_members):
        # Mock the CSV reader and writer
        mock_csvfile = MagicMock()
        mock_writer_instance = MagicMock()
        mock_writer.return_value = mock_writer_instance

        csv_content = [
            ["Test Band"],
            ["Another Band"]
        ]
        
        with patch('builtins.open', unittest.mock.mock_open(read_data='\n'.join([','.join(row) for row in csv_content]))):
            band.process_artist_file('mock_input.csv', 'mock_output.csv')

            # Check if writerow was called with the correct arguments
            mock_writer_instance.writerow.assert_any_call(["Artist", "Member"])
            mock_writer_instance.writerow.assert_any_call(["Test Band", "Member 1"])
            mock_writer_instance.writerow.assert_any_call(["Test Band", "Member 2"])
            mock_writer_instance.writerow.assert_any_call(["Another Band", "Member 1"])
            mock_writer_instance.writerow.assert_any_call(["Another Band", "Member 2"])

if __name__ == '__main__':
    unittest.main()