import unittest
from unittest.mock import patch, mock_open, MagicMock
from get_venues_from_setlistfm_v2 import fetch_venues_data, write_xml_to_file, convert_xml_to_csv

class TestGetVenuesFromSetlistfm(unittest.TestCase):

    @patch('get_venues_from_setlistfm_v2.requests.get')
    def test_fetch_venues_data_success(self, mock_get):
        # Mocking the requests.get response for 3 pages
        mock_responses = [
            MagicMock(status_code=200, text='<venue id="1" name="Venue1"></venue>'),
            MagicMock(status_code=200, text='<venue id="2" name="Venue2"></venue>'),
            MagicMock(status_code=200, text='<venue id="3" name="Venue3"></venue>'),
            MagicMock(status_code=200, text='')  # No data on the 4th page to stop the loop
        ]
        
        mock_get.side_effect = mock_responses

        url = "https://api.setlist.fm/rest/1.0/search/venues"
        headers = {
            "Accept": "application/xml",
            "x-api-key": "test-api-key"
        }
        
        # Call the function
        data = fetch_venues_data(url, headers)
        
        # Assertions
        self.assertEqual(len(data), 3)
        self.assertIn('<venue id="1" name="Venue1"></venue>', data)
        self.assertIn('<venue id="2" name="Venue2"></venue>', data)
        self.assertIn('<venue id="3" name="Venue3"></venue>', data)
    
    @patch('get_venues_from_setlistfm_v2.requests.get')
    def test_fetch_venues_data_no_data(self, mock_get):
        # Mocking the requests.get response with no data
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = ''
        mock_get.return_value = mock_response

        url = "https://api.setlist.fm/rest/1.0/search/venues"
        headers = {
            "Accept": "application/xml",
            "x-api-key": "test-api-key"
        }
        
        # Call the function
        data = fetch_venues_data(url, headers)
        
        # Assertions
        self.assertEqual(len(data), 0)
    
    @patch('builtins.open', new_callable=mock_open)
    def test_write_xml_to_file(self, mock_open):
        xml_data = ['<venue id="1" name="Venue1"></venue>']
        filename = "test_venues.xml"
        
        # Call the function
        write_xml_to_file(xml_data, filename)
        
        # Assertions
        mock_open.assert_called_once_with(filename, 'w', encoding='utf-8-sig')
        handle = mock_open()
        handle.write.assert_any_call('<?xml version="1.0" encoding="UTF-8"?>\n<venues>\n')
        handle.write.assert_any_call('<venue id="1" name="Venue1"></venue>')
        handle.write.assert_any_call('</venues>\n')
    
    @patch('builtins.open', new_callable=mock_open, read_data='<venue id="1" name="Venue1"></venue>\n<city id="1" name="London"></city>\n<coords lat="51.5074" long="-0.1278"></coords>\n')
    def test_convert_xml_to_csv(self, mock_open):
        xml_filename = "test_venues.xml"
        csv_filename = "test_venues.csv"
        
        # Call the function
        convert_xml_to_csv(xml_filename, csv_filename)
        
        # Assertions
        mock_open.assert_any_call(xml_filename, 'r', encoding='utf-8-sig')
        mock_open.assert_any_call(csv_filename, 'w', newline='', encoding='utf-8')
        handle = mock_open()
        handle.write.assert_any_call("Venue ID,Venue Name,City Name,Latitude,Longitude\r\n")
        handle.write.assert_any_call("1,Venue1,London,51.5074,-0.1278\r\n")

if __name__ == '__main__':
    unittest.main()