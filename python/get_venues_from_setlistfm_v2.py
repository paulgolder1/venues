import requests
import re
import csv
import time

def fetch_venues_data(url, headers):
    
    # Fetch all venues data for GB across all pages.
    
    data = []
    page = 1  # Start from the first page

    while True:
        params = {"country": "GB", "p": page}
        response = requests.get(url, headers=headers, params=params)
        
        # Log the status code and response content for debugging
        print(f"Fetching page {page}...")
        if response.status_code == 200:
            print(f"Response Content for Page {page}: {response.text[:500]}")  # First 500 chars for debugging
            response_text = re.sub(r'<\?xml.*?\?>', '', response.text)
            if not response_text.strip():
                print(f"No data on page {page}. Stopping.")
                break  # Stop fetching when no data is returned
            data.append(response_text)
            time.sleep(2)  # Pause to avoid rate limiting
            page += 1  # Go to the next page
        else:
            print(f"Failed to fetch page {page} with HTTP status {response.status_code}")
            break  # Stop fetching on error

    return data

def write_xml_to_file(xml_data, filename):
    
    # Write the XML data to a file.
    
    with open(filename, "w", encoding="utf-8-sig") as xml_file:
        xml_file.write('<?xml version="1.0" encoding="UTF-8"?>\n<venues>\n')
        for data in xml_data:
            xml_file.write(data)
        xml_file.write('</venues>\n')

def convert_xml_to_csv(xml_filename, csv_filename):
    
    # Convert XML data to CSV format with venue ID, venue name, city name, latitude, and longitude.
    
    with open(xml_filename, "r", encoding="utf-8-sig") as xml_file, open(csv_filename, "w", newline="", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["Venue ID", "Venue Name", "City Name", "Latitude", "Longitude"])

        venue_id = venue = city = lat = long = None
        for line in xml_file:
            line = line.replace("&amp;", "&")
            try:
                if line.strip().startswith('<venue id'):
                    venue_id_match = re.search(r'id="([^"]+)"', line)
                    venue_name_match = re.search(r'name="([^"]+)"', line)
                    venue_id = venue_id_match.group(1) if venue_id_match else None
                    venue = venue_name_match.group(1) if venue_name_match else None

                elif line.strip().startswith('<city id'):
                    city_match = re.search(r'name="([^"]+)"', line)
                    city = city_match.group(1) if city_match else None

                elif line.strip().startswith('<coords'):
                    lat_match = re.search(r'lat="([^"]+)"', line)
                    long_match = re.search(r'long="([^"]+)"', line)
                    lat = lat_match.group(1) if lat_match else None
                    long = long_match.group(1) if long_match else None

                    # Print venue data for debugging
                    print(f"Writing to CSV: {venue_id}, {venue}, {city}, {lat}, {long}")
                    
                    # Write to CSV if all fields are available
                    if venue_id and venue and city and lat and long:
                        writer.writerow([venue_id, venue, city, lat, long])
                        venue_id = venue = city = lat = long = None  # Reset variables for the next venue

            except Exception as e:
                print(f"Warning: Skipping a malformed entry due to error: {e}")

if __name__ == "__main__":
    # Parameters
    url = "https://api.setlist.fm/rest/1.0/search/venues"
    headers = {
        "Accept": "application/xml",
        "x-api-key": "jQrCY2Wmf2gIGQA4ABzVeWduFG15p8HkVpkn"
    }
    xml_filename = "all_venues.xml"
    csv_filename = "all_venues.csv"

    try:
        # Fetch venue data for GB
        print(f"Fetching venue data for venues in GB...")
        xml_data = fetch_venues_data(url, headers)
        
        # Write XML data to file
        print(f"Writing XML data to {xml_filename}...")
        write_xml_to_file(xml_data, xml_filename)
        
        # Convert XML to CSV
        print(f"Converting XML data to CSV format in {csv_filename}...")
        convert_xml_to_csv(xml_filename, csv_filename)
        
        print("Script completed successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")
