import requests
import csv
import time
import math

def get_band_members(band_name):
    
    # Fetches band members of a given band name using the MusicBrainz API.

    base_url = "https://musicbrainz.org/ws/2/artist/"
    params = {
        "query": band_name,
        "fmt": "json"
    }

    # Search for the band
    response = requests.get(base_url, params=params)
    if response.status_code != 200:
        print(f"Error: Unable to fetch data for {band_name}. Status code {response.status_code}")
        return []

    results = response.json().get('artists', [])
    if not results:
        print(f"No results found for {band_name}.")
        return []

    # Find the most relevant band (first result)
    band = results[0]
    band_id = band['id']

    # Get details of the band, including members
    response = requests.get(f"{base_url}{band_id}?inc=artist-rels&fmt=json")
    if response.status_code != 200:
        print(f"Error: Unable to fetch band details for {band_name}. Status code {response.status_code}")
        return []

    details = response.json()
    members = [
        relation['artist']['name']
        for relation in details.get('relations', [])
        if relation['type'] == 'member of band'
    ]
    return members

def format_time_remaining(seconds):
    
    # A script to estimate time remaining before completion of execution of the script
    
    if seconds >= 60:
        minutes = seconds // 60
        remaining_seconds = seconds % 60
        return f"{minutes} minutes {remaining_seconds} seconds" if remaining_seconds else f"{minutes} minutes"
    else:
        return f"{seconds} seconds"

def process_artist_file(input_file, output_file):
    """
    Reads artists from a CSV file, fetches their band members, and writes the results to another CSV file.

    Args:
        input_file (str): Path to the input CSV file containing artist names.
        output_file (str): Path to the output CSV file for saving band members.
    """
    checked_artists = set()

    # Count total lines in the input file
    with open(input_file, 'r', encoding='utf-8') as infile:
        total_lines = sum(1 for _ in infile)

    with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', newline='', encoding='utf-8') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)
        writer.writerow(["Artist", "Member"])  # Write header row

        processed_count = 0
        for row in reader:
            artist_name = row[0]
            if artist_name in checked_artists:
                continue

            checked_artists.add(artist_name)
            processed_count += 1
            print(f"Fetching members for {artist_name} ({processed_count}/{total_lines})...")

            # Estimate remaining time
            remaining_items = total_lines - processed_count
            remaining_time = remaining_items * 1.5
            formatted_time = format_time_remaining(math.ceil(remaining_time))
            print(f"Estimated time remaining: {formatted_time}")

            members = get_band_members(artist_name)

            # Wait for 1.5 seconds before the next API call
            time.sleep(1.5)

            for member in members:
                writer.writerow([artist_name, member])
            if not members:
                print(f"No members found for {artist_name}.")

def main():
    """
    Main function to process artist genres and fetch band members.
    """
    input_file = 'artist_genres.csv'
    output_file = 'artist_members.csv'

    print("Starting the process of fetching band members...")
    process_artist_file(input_file, output_file)
    print(f"Process complete. Results saved to {output_file}.")

# Run the script
if __name__ == "__main__":
    main()
