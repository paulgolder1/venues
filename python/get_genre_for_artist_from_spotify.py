import csv
import requests
import base64
import time 

# Spotify API credentials
client_id = 'ebf11efffb0945f691c2321f9a43d17d'
client_secret = '33c388120aad4454824c2048d80fa8ce'

def get_spotify_access_token(client_id, client_secret):
    
    # Get the access token from Spotify API using client credentials
    
    auth_url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + base64.b64encode(f"{client_id}:{client_secret}".encode()).decode("utf-8"),
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "grant_type": "client_credentials"
    }

    response = requests.post(auth_url, headers=headers, data=data)
    
    if response.status_code == 200:
        access_token = response.json()['access_token']
        return access_token
    else:
        print(f"Failed to get access token: {response.status_code}")
        return None

def get_artist_genres(artist_name, access_token):
    
    # Fetch the genres of an artist from the Spotify API
    
    search_url = f"https://api.spotify.com/v1/search?q={artist_name}&type=artist&limit=1"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    
    response = requests.get(search_url, headers=headers)
    
    if response.status_code == 200:
        artist_data = response.json()
        if artist_data['artists']['items']:
            artist = artist_data['artists']['items'][0]
            genres = artist.get('genres', [])
            return genres
        else:
            print(f"No artist found for {artist_name}")
            return []
    else:
        print(f"Failed to fetch artist data: {response.status_code}")
        return []

def get_unique_artists_from_csv(csv_filename):
    
    # Read artist names from the CSV file and return a unique list
    
    artist_names = set()
    with open(csv_filename, "r", encoding="utf-8") as csv_file:
        reader = csv.reader(csv_file)
        next(reader)  # Skip header row
        for row in reader:
            artist_names.add(row[1])  # Artist Name is in the second column
    return list(artist_names)

def save_genres_to_csv(artist_genres, output_filename):
    
    # Save the artist genres to a CSV file
    
    with open(output_filename, "w", newline="", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["Artist Name", "Genre"])  # Write the header row
        
        # Write each artist's genre
        for artist_name, genres in artist_genres:
            for genre in genres:
                writer.writerow([artist_name, genre])

def main():
    csv_filename = "shows.csv"  # Input CSV file containing artist names
    access_token = get_spotify_access_token(client_id, client_secret)
    
    if access_token:
        # Get unique artist names from shows.csv
        artists = get_unique_artists_from_csv(csv_filename)
        print(f"Found {len(artists)} unique artists.")

        # List to store artist genre data
        artist_genres = []

        # Iterate through the artist list and get genres
        for artist_name in artists:
            print(f"Fetching genres for {artist_name}...")
            genres = get_artist_genres(artist_name, access_token)
            if genres:
                artist_genres.append((artist_name, genres))
            else:
                print(f"No genres found for {artist_name}.")

            # Sleep for 0.5 seconds between each API call to avoid rate limits
            time.sleep(0.5)

        # Save the artist genres to a CSV file
        if artist_genres:
            print("Saving genres to artist_genres.csv...")
            save_genres_to_csv(artist_genres, "artist_genres.csv")
            print("Data saved successfully.")
        else:
            print("No data to save.")
    else:
        print("Error: Unable to fetch access token.")

if __name__ == "__main__":
    main()
