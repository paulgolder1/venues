import csv

def remove_duplicates(input_file, output_file):
    
    # Removes duplicate lines from a CSV file and saves the cleaned file.

    try:
        # Read the file and store unique rows
        seen = set()
        cleaned_lines = []
        
        with open(input_file, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                row_tuple = tuple(row)  # Convert list to tuple for set comparison
                if row_tuple not in seen:
                    seen.add(row_tuple)
                    cleaned_lines.append(row)
        
        # Write cleaned lines to the output file
        with open(output_file, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerows(cleaned_lines)
        
        print(f"Duplicates removed. Cleaned file saved to: {output_file}")
    
    except Exception as e:
        print(f"Error: {e}")

# Process script
input_file = "artist_members.csv"
output_file = "artist_members_cleaned.csv"
remove_duplicates(input_file, output_file)
