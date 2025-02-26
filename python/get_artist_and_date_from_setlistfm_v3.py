import requests
import csv
from datetime import datetime
import time

def fetch_venue_setlists_by_id(venue_id, headers):
    # Fetch setlists for a given venue ID from Setlist.fm, handling pagination.
    url = f"https://api.setlist.fm/rest/1.0/venue/{venue_id}/setlists"
    all_setlists = []
    page = 1

    while True:
        params = {"p": page}
        response = requests.get(url, headers=headers, params=params)

        if response.status_code == 200:
            data = response.json()
            if 'setlist' in data and data['setlist']:
                all_setlists.extend(data['setlist'])
                page += 1
                time.sleep(0.5)  # Pause to avoid rate limiting
            else:
                break  # No more data to fetch
        elif response.status_code == 404:
            message = response.json().get('message', '')
            if 'page does not exist' in message:
                break  # Stop pagination as the page does not exist
            else:
                print(f"Failed to fetch setlists for venue {venue_id}. HTTP status code: {response.status_code}")
                print(f"Response content: {response.content}")  # Print response content for debugging
                break
        else:
            print(f"Failed to fetch setlists for venue {venue_id}. HTTP status code: {response.status_code}")
            print(f"Response content: {response.content}")  # Print response content for debugging
            break

    return all_setlists

# Other functions remain the same

def extract_band_names_and_dates(setlist_data):
    # Extract band names and show dates from the setlist data.
    if not setlist_data:
        print("No setlist data available.")
        return []

    bands_and_dates = []

    for show in setlist_data:
        artist = show.get('artist', {}).get('name', 'Unknown Artist')
        event_date = show.get('eventDate', 'Unknown Date')

        # If the date is present, try to format it or leave it as-is
        try:
            event_date = datetime.strptime(event_date, '%Y-%m-%d').strftime('%Y-%m-%d')
        except ValueError:
            # Keep the raw event date instead of defaulting to 'Unknown Date'
            pass
        
        bands_and_dates.append((artist, event_date))

    return bands_and_dates

def get_venue_ids_from_csv(csv_filename):
    # Read venue IDs from the given CSV file.
    venue_ids = []
    with open(csv_filename, "r", encoding="utf-8") as csv_file:
        reader = csv.reader(csv_file)
        next(reader)  # Skip header row
        for row in reader:
            venue_ids.append(row[0])  # Assuming the Venue ID is in the first column
    return venue_ids

def save_to_csv(data, output_filename):
    # Save the extracted data to a CSV file.
    with open(output_filename, "w", newline="", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["Venue ID", "Artist", "Date"])  # Write the header row

        # Write each row of data
        for venue_id, artist, date in data:
            writer.writerow([venue_id, artist, date])

def main():
    headers = {
        "Accept": "application/json",
        "x-api-key": "jQrCY2Wmf2gIGQA4ABzVeWduFG15p8HkVpkn" 
    }

    # Get all venue IDs from the CSV file
    csv_filename = "all_venues.csv"
    venue_ids = get_venue_ids_from_csv(csv_filename)

    if not venue_ids:
        print("No venue IDs found in the CSV file.")
        return

    # List to store all the extracted data
    all_shows_data = []
    total_venues = len(venue_ids)

    # Track the start time for progress and estimated time
    start_time = time.time()

    # Iterate over each venue ID and fetch setlist data
    for i, venue_id in enumerate(venue_ids, 1):
        print(f"Fetching setlists for venue ID {venue_id} ({i}/{total_venues})...")
        setlist_data = fetch_venue_setlists_by_id(venue_id, headers)

        # Extract band names and show dates
        bands_and_dates = extract_band_names_and_dates(setlist_data)

        if bands_and_dates:
            for artist, date in bands_and_dates:
                all_shows_data.append((venue_id, artist, date))
        else:
            print(f"No setlists found for venue ID {venue_id}.")

        # Show progress and estimated time remaining
        elapsed_time = time.time() - start_time
        avg_time_per_venue = elapsed_time / i
        remaining_venues = total_venues - i
        estimated_time_remaining = avg_time_per_venue * remaining_venues
        minutes_remaining = estimated_time_remaining / 60
        print(f"Progress: {i}/{total_venues} | Estimated Time Remaining: {minutes_remaining:.2f} minutes")

        # Wait 0.5 seconds before making the next request
        time.sleep(0.5)

    # Save the extracted data to shows.csv
    if all_shows_data:
        print("Saving data to shows.csv...")
        save_to_csv(all_shows_data, "shows.csv")
        print("Data saved successfully.")
    else:
        print("No data to save.")

if __name__ == "__main__":
    main()