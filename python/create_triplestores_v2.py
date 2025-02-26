import csv
from rdflib import Graph, Literal, Namespace, RDF, URIRef
from urllib.parse import quote

# Define namespaces with generic websites
EX = Namespace("http://example.org/")
SCHEMA = Namespace("http://schema.org/")

# Initialize the RDF graph
g = Graph()

# Bind namespaces
g.bind("ex", EX)
g.bind("schema", SCHEMA)

# Helper function to sanitize and create URIs
def create_uri(namespace, name):
    sanitized_name = quote(name.replace(" ", "_").replace(",", "").lower(), safe="_")
    return URIRef(f"{namespace}{sanitized_name}")

def main():
    # 1. Load all_venues.csv
    with open("all_venues.csv", "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            venue_uri = create_uri(EX, row["Venue ID"])
            g.add((venue_uri, RDF.type, SCHEMA.MusicVenue))
            g.add((venue_uri, SCHEMA.name, Literal(row["Venue Name"])))
            g.add((venue_uri, SCHEMA.addressLocality, Literal(row["City Name"])))
            g.add((venue_uri, SCHEMA.geo, Literal(f"{row['Latitude']},{row['Longitude']}")))

    # 2. Load shows.csv
    with open("shows.csv", "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            show_uri = create_uri(EX, f"show_{row['Venue ID']}_{row['Date']}")
            venue_uri = create_uri(EX, row["Venue ID"])
            artist_uri = create_uri(EX, row["Artist"])
            g.add((show_uri, RDF.type, SCHEMA.Event))
            g.add((show_uri, SCHEMA.location, venue_uri))
            g.add((show_uri, SCHEMA.performer, artist_uri))
            g.add((show_uri, SCHEMA.performanceDate, Literal(row["Date"])))

    # 3. Load artist_genres.csv
    with open("artist_genres.csv", "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            artist_uri = create_uri(EX, row["Artist Name"])
            genre_uri = create_uri(EX, row["Genre"])
            g.add((artist_uri, RDF.type, SCHEMA.MusicGroup))
            g.add((artist_uri, SCHEMA.genre, genre_uri))
            g.add((genre_uri, RDF.type, SCHEMA.Genre))
            g.add((genre_uri, SCHEMA.name, Literal(row["Genre"])))

    # 4. Load artist_members_cleaned.csv
    with open("artist_members_cleaned.csv", "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            artist_uri = create_uri(EX, row["Artist"])
            member_uri = create_uri(EX, row["Member"])
            g.add((artist_uri, SCHEMA.member, member_uri))
            g.add((member_uri, RDF.type, SCHEMA.Person))
            g.add((member_uri, SCHEMA.name, Literal(row["Member"])))

    # Save the graph to a file
    output_file = "linked_data_triplestore.ttl"
    g.serialize(destination=output_file, format="turtle")

    print(f"Triplestore created and saved to {output_file}")

if __name__ == "__main__":
    main()