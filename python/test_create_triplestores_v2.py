import unittest
import csv
import os
from rdflib import Graph, URIRef, Literal, Namespace, RDF
from create_triplestores_v2 import create_uri, main

# Define namespaces for testing
EX = Namespace("http://example.org/")
SCHEMA = Namespace("http://schema.org/")

class TestLinkedData(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Create test CSV files
        cls.create_test_csv_files()

    @classmethod
    def tearDownClass(cls):
        # Clean up test CSV files
        cls.cleanup_test_csv_files()

    @classmethod
    def create_test_csv_files(cls):
        # Create all_venues.csv
        with open("all_venues.csv", "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=["Venue ID", "Venue Name", "City Name", "Latitude", "Longitude"])
            writer.writeheader()
            writer.writerow({
                "Venue ID": "venue1",
                "Venue Name": "Venue One",
                "City Name": "City A",
                "Latitude": "1.23",
                "Longitude": "4.56"
            })

        # Create shows.csv
        with open("shows.csv", "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=["Venue ID", "Date", "Artist"])
            writer.writeheader()
            writer.writerow({
                "Venue ID": "venue1",
                "Date": "01-02-2025",
                "Artist": "Artist A"
            })

        # Create artist_genres.csv
        with open("artist_genres.csv", "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=["Artist Name", "Genre"])
            writer.writeheader()
            writer.writerow({
                "Artist Name": "Artist A",
                "Genre": "Rock"
            })

        # Create artist_members_cleaned.csv
        with open("artist_members_cleaned.csv", "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=["Artist", "Member"])
            writer.writeheader()
            writer.writerow({
                "Artist": "Artist A",
                "Member": "Member 1"
            })

    @classmethod
    def cleanup_test_csv_files(cls):
        # Remove test CSV files
        os.remove("all_venues.csv")
        os.remove("shows.csv")
        os.remove("artist_genres.csv")
        os.remove("artist_members_cleaned.csv")
        os.remove("linked_data_triplestore.ttl")

    def test_create_uri(self):
        # Test the create_uri function
        uri = create_uri(EX, "Test Name")
        self.assertEqual(uri, URIRef("http://example.org/test_name"))

    def test_main(self):
        # Run the main function
        main()

        # Load the generated RDF graph
        g = Graph()
        g.parse("linked_data_triplestore.ttl", format="turtle")

        # Check venue data
        venue_uri = create_uri(EX, "venue1")
        self.assertIn((venue_uri, RDF.type, SCHEMA.MusicVenue), g)
        self.assertIn((venue_uri, SCHEMA.name, Literal("Venue One")), g)
        self.assertIn((venue_uri, SCHEMA.addressLocality, Literal("City A")), g)
        self.assertIn((venue_uri, SCHEMA.geo, Literal("1.23,4.56")), g)

        # Check show data
        show_uri = create_uri(EX, "show_venue1_01-02-2025")
        self.assertIn((show_uri, RDF.type, SCHEMA.Event), g)
        self.assertIn((show_uri, SCHEMA.location, venue_uri), g)
        self.assertIn((show_uri, SCHEMA.performer, create_uri(EX, "Artist A")), g)
        self.assertIn((show_uri, SCHEMA.performanceDate, Literal("01-02-2025")), g)

        # Check artist genre data
        artist_uri = create_uri(EX, "Artist A")
        genre_uri = create_uri(EX, "Rock")
        self.assertIn((artist_uri, RDF.type, SCHEMA.MusicGroup), g)
        self.assertIn((artist_uri, SCHEMA.genre, genre_uri), g)
        self.assertIn((genre_uri, RDF.type, SCHEMA.Genre), g)
        self.assertIn((genre_uri, SCHEMA.name, Literal("Rock")), g)

        # Check artist member data
        member_uri = create_uri(EX, "Member 1")
        self.assertIn((artist_uri, SCHEMA.member, member_uri), g)
        self.assertIn((member_uri, RDF.type, SCHEMA.Person), g)
        self.assertIn((member_uri, SCHEMA.name, Literal("Member 1")), g)

if __name__ == "__main__":
    unittest.main()