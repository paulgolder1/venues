<?php include ('header.php') ?>


This is my venue website!
<br /><br />
Here's a few things I've written over the years.
<br /><br />

<?php
function haversineDistance($lat1, $lon1, $lat2, $lon2) {
    $earthRadius = 3958.8; // Earth's radius in miles
    $dLat = deg2rad($lat2 - $lat1);
    $dLon = deg2rad($lon2 - $lon1);
    $a = sin($dLat / 2) ** 2 +
         cos(deg2rad($lat1)) * cos(deg2rad($lat2)) * sin($dLon / 2) ** 2;
    $c = 2 * atan2(sqrt($a), sqrt(1 - $a));
    return $earthRadius * $c;
}

// Replace with actual user latitude and longitude
$userLat = 52.6498; // Example: Your latitude
$userLon = -3.3212;  // Example: Your longitude

// Load the Turtle file
$turtleFile = file_get_contents('data/linked_data_triplestore.ttl');

// Parse the Turtle file
$pattern = '/ex:[^ ]+ a schema1:MusicVenue ;\s+schema1:addressLocality "([^"]+)" ;\s+schema1:geo "([^"]+)" ;\s+schema1:name "([^"]+)" ./';
preg_match_all($pattern, $turtleFile, $matches, PREG_SET_ORDER);

// Process each venue
$venues = [];
foreach ($matches as $match) {
    $locality = $match[1];
    [$lat, $lon] = explode(',', $match[2]);
    $name = $match[3];

    // Calculate distance
    $distance = haversineDistance($userLat, $userLon, (float)$lat, (float)$lon);
    $venues[] = [
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
echo "<h1>20 Nearest Music Venues</h1>";
echo "<table border='1'>
        <tr>
            <th>Name</th>
            <th>Locality</th>
            <th>Latitude</th>
            <th>Longitude</th>
            <th>Distance (miles)</th>
        </tr>";
foreach ($nearestVenues as $venue) {
    echo "<tr>
            <td>{$venue['name']}</td>
            <td>{$venue['locality']}</td>
            <td>{$venue['lat']}</td>
            <td>{$venue['lon']}</td>
            <td>" . number_format($venue['distance'], 2) . "</td>
        </tr>";
}
echo "</table>";
?>



<?php include ('footer.php') ?>

