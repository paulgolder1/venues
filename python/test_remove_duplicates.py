import unittest
from unittest.mock import mock_open, patch
from io import StringIO
import csv
from remove_duplicates import remove_duplicates

class TestRemoveDuplicates(unittest.TestCase):

    @patch("builtins.open", new_callable=mock_open)
    @patch("csv.reader")
    @patch("csv.writer")
    def test_remove_duplicates_no_duplicates(self, mock_writer, mock_reader, mock_open):
        # Mock input CSV data with no duplicates
        mock_reader.return_value = [
            ["name", "instrument"],
            ["Paul Golder", "Vocals"],
            ["Sharon Golder", "Guitar"],
            ["Alex Golder", "Drums"]
        ]
        
        # Call the function
        remove_duplicates("input.csv", "output.csv")
        
        # Check that the output file was written with the same data
        mock_writer().writerows.assert_called_once_with([
            ["name", "instrument"],
            ["Paul Golder", "Vocals"],
            ["Sharon Golder", "Guitar"],
            ["Alex Golder", "Drums"]
        ])

    @patch("builtins.open", new_callable=mock_open)
    @patch("csv.reader")
    @patch("csv.writer")
    def test_remove_duplicates_with_duplicates(self, mock_writer, mock_reader, mock_open):
        # Mock input CSV data with duplicates
        mock_reader.return_value = [
            ["name", "instrument"],
            ["Paul Golder", "Vocals"],
            ["Sharon Golder", "Guitar"],
            ["Paul Golder", "Vocals"],
            ["Paul Golder", "Vocals"],
            ["Sharon Golder", "Guitar"],
            ["Alex Golder", "Drums"]
        ]
        
        # Call the function
        remove_duplicates("input.csv", "output.csv")
        
        # Check that the output file was written without duplicates
        mock_writer().writerows.assert_called_once_with([
            ["name", "instrument"],
            ["Paul Golder", "Vocals"],
            ["Sharon Golder", "Guitar"],
            ["Alex Golder", "Drums"]
        ])

    @patch("builtins.open", new_callable=mock_open)
    @patch("csv.reader")
    @patch("csv.writer")
    def test_remove_duplicates_empty_file(self, mock_writer, mock_reader, mock_open):
        # Mock input CSV data as an empty file
        mock_reader.return_value = []
        
        # Call the function
        remove_duplicates("input.csv", "output.csv")
        
        # Check that the output file was written as empty
        mock_writer().writerows.assert_called_once_with([])

    @patch("builtins.open", new_callable=mock_open)
    @patch("csv.reader")
    @patch("csv.writer")
    def test_remove_duplicates_io_error(self, mock_writer, mock_reader, mock_open):
        # Mock an IOError during file operations
        mock_open.side_effect = IOError("Unable to open file")
        
        # Capture the output to check for error message
        with patch('sys.stdout', new=StringIO()) as fake_out:
            remove_duplicates("input.csv", "output.csv")
            self.assertIn("Error: Unable to open file", fake_out.getvalue())

if __name__ == '__main__':
    unittest.main()