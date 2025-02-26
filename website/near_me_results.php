<?php include('header.php'); ?>

<h1>Locations near me</h1>

<?php
// Get the search query from the URL
$query = isset($_GET['q']) ? strtolower(trim($_GET['q'])) : '';

// Function to remove spaces and convert to lowercase
function normalize($string) {
    return strtolower(str_replace(' ', '', $string));
}

// Check if query is provided
if ($query) {
    echo "<p>You searched for: <strong>" . htmlspecialchars($query) . "</strong></p>";

    // Open the CSV file
    $file = fopen('data/ukpostcodes.csv', 'r');
    if ($file !== false) {
        $found = false;
        while (($line = fgetcsv($file)) !== false) {
            // CSV structure is: id, Postcode, latitude, longitude
            $postcode = normalize($line[1]); // normalize the postcode field
            $search_query = normalize($query);

            // Check if the normalized postcode matches the search query
            if ($postcode == $search_query) {
                // Convert latitude and longitude to floats
                $userLat = (float)$line[2];
                $userLon = (float)$line[3];
                $found = true;
            }
        }

        // If no match found
        if (!$found) {
            echo "<p>No results found for '$query'.</p>";
			exit;
        }

        fclose($file);
    } else {
        echo "<p>Could not open the file.</p>";
    }
} else {
    echo "<p>Please enter a location to search.</p>";
}

function haversineDistance($lat1, $lon1, $lat2, $lon2) {
    $earthRadius = 3958.8; // Earth's radius in miles
    $dLat = deg2rad($lat2 - $lat1);
    $dLon = deg2rad($lon2 - $lon1);
    $a = sin($dLat / 2) ** 2 +
         cos(deg2rad($lat1)) * cos(deg2rad($lat2)) * sin($dLon / 2) ** 2;
    $c = 2 * atan2(sqrt($a), sqrt(1 - $a));
    return $earthRadius * $c;
}

// Load the Turtle file
$turtleFile = file_get_contents('data/linked_data_triplestore.ttl');

// Parse the Turtle file
// Update the regex to capture just the ID (exclude "ex:")
$pattern = '/ex:([a-z0-9]+) a schema1:MusicVenue ;\s+schema1:addressLocality "([^"]+)" ;\s+schema1:geo "([^"]+)" ;\s+schema1:name "([^"]+)" ./';
preg_match_all($pattern, $turtleFile, $matches, PREG_SET_ORDER);

// Process each venue
$venues = [];
foreach ($matches as $match) {
    $venueId = $match[1]; // Capture the ID without the "ex:"
    $locality = $match[2];
    [$lat, $lon] = explode(',', $match[3]);
    $name = $match[4];

    // Calculate distance
    $distance = haversineDistance($userLat, $userLon, (float)$lat, (float)$lon);
    $venues[] = [
        'id' => $venueId,  // Store the venue ID
        'name' => $name,
        'locality' => $locality,
        'lat' => (float)$lat,
        'lon' => (float)$lon,
        'distance' => $distance
    ];
}

// Sort venues by distance
usort($venues, fn($a, $b) => $a['distance'] <=> $b['distance']);

// Get the 20 nearest venues
$nearestVenues = array_slice($venues, 0, 20);

// Display results
echo "Here are the nearest music venues:<br /><br />";
echo "<table border='1' cellpadding='3' style='border-collapse: collapse;'>";
echo "<tr>
        <th>Venue</th>
        <th>Distance (miles)</th>
    </tr>";
foreach ($nearestVenues as $venue) {
    echo "<tr>
        <td>
		<a href='details.php?q=" . $venue['id'] . "'>
		{$venue['name']}, {$venue['locality']}
		</a>
		</td>
        <td style='text-align: right;'>" . number_format($venue['distance'], 2) . "</td>
        </tr>";
}
echo "</table>";
?>

<?php include('footer.php'); ?>
