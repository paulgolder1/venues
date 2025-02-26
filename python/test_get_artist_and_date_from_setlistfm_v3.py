import unittest
from unittest.mock import patch, mock_open, MagicMock
from get_artist_and_date_from_setlistfm_v3 import fetch_venue_setlists_by_id, extract_band_names_and_dates, get_venue_ids_from_csv, save_to_csv, main

class TestGetArtistAndDateFromSetlistfm(unittest.TestCase):

    @patch('get_artist_and_date_from_setlistfm_v3.requests.get')
    def test_fetch_venue_setlists_by_id_success(self, mock_get):
        # Mocking the requests.get response for 3 pages
        mock_responses = [
            MagicMock(status_code=200, json=lambda: {'setlist': [{'artist': {'name': 'Artist1'}, 'eventDate': '2022-01-01'}]}),
            MagicMock(status_code=200, json=lambda: {'setlist': [{'artist': {'name': 'Artist2'}, 'eventDate': '2022-01-02'}]}),
            MagicMock(status_code=200, json=lambda: {'setlist': [{'artist': {'name': 'Artist3'}, 'eventDate': '2022-01-03'}]}),
            MagicMock(status_code=200, json=lambda: {'setlist': []})  # No data on the 4th page to stop the loop
        ]
        
        mock_get.side_effect = mock_responses

        venue_id = "test_venue_id"
        headers = {
            "Accept": "application/json",
            "x-api-key": "test-api-key"
        }
        
        # Call the function
        setlists = fetch_venue_setlists_by_id(venue_id, headers)
        
        # Assertions
        self.assertEqual(len(setlists), 3)
        self.assertIn({'artist': {'name': 'Artist1'}, 'eventDate': '2022-01-01'}, setlists)
        self.assertIn({'artist': {'name': 'Artist2'}, 'eventDate': '2022-01-02'}, setlists)
        self.assertIn({'artist': {'name': 'Artist3'}, 'eventDate': '2022-01-03'}, setlists)
    
    def test_extract_band_names_and_dates(self):
        setlist_data = [
            {'artist': {'name': 'Artist1'}, 'eventDate': '2022-01-01'},
            {'artist': {'name': 'Artist2'}, 'eventDate': '2022-01-02'},
            {'artist': {'name': 'Artist3'}, 'eventDate': '2022-01-03'}
        ]
        
        # Call the function
        bands_and_dates = extract_band_names_and_dates(setlist_data)
        
        # Assertions
        self.assertEqual(len(bands_and_dates), 3)
        self.assertIn(('Artist1', '2022-01-01'), bands_and_dates)
        self.assertIn(('Artist2', '2022-01-02'), bands_and_dates)
        self.assertIn(('Artist3', '2022-01-03'), bands_and_dates)
    
    @patch('builtins.open', new_callable=mock_open, read_data="Venue ID\n1\n2\n3\n")
    def test_get_venue_ids_from_csv(self, mock_open):
        csv_filename = "test_venues.csv"
        
        # Call the function
        venue_ids = get_venue_ids_from_csv(csv_filename)
        
        # Assertions
        self.assertEqual(len(venue_ids), 3)
        self.assertIn('1', venue_ids)
        self.assertIn('2', venue_ids)
        self.assertIn('3', venue_ids)
    
    @patch('builtins.open', new_callable=mock_open)
    def test_save_to_csv(self, mock_open):
        data = [('1', 'Artist1', '2022-01-01'), ('2', 'Artist2', '2022-01-02'), ('3', 'Artist3', '2022-01-03')]
        output_filename = "test_shows.csv"
        
        # Call the function
        save_to_csv(data, output_filename)
        
        # Assertions
        mock_open.assert_called_once_with(output_filename, 'w', newline='', encoding='utf-8')
        handle = mock_open()
        handle.write.assert_any_call('Venue ID,Artist,Date\r\n')
        handle.write.assert_any_call('1,Artist1,2022-01-01\r\n')
        handle.write.assert_any_call('2,Artist2,2022-01-02\r\n')
        handle.write.assert_any_call('3,Artist3,2022-01-03\r\n')

if __name__ == '__main__':
    unittest.main()

    