<?

// Regex pattern to match MusicVenue entries with ID, addressLocality, geo, and name
$pattern = '/ex:([^ ]+) a schema1:MusicVenue ;\s+schema1:addressLocality "([^"]+)" ;\s+schema1:geo "([^"]+)" ;\s+schema1:name "([^"]+)" ./';
preg_match_all($pattern, $turtleFile, $matches, PREG_SET_ORDER);

// Filter venues based on query
$results = [];
foreach ($matches as $match) {
    $id = $match[1];         // ID (e.g., 13d10d31)
    $locality = strtolower($match[2]); // addressLocality
    $name = strtolower($match[4]);    // name

    // Check if query matches either name or locality
    if (strpos($locality, $query) !== false || strpos($name, $query) !== false) {
        $results[] = [
            'id' => $id,
            'name' => $match[4],
            'locality' => $match[2],
        ];
    }
}

// Sort results alphabetically by name
usort($results, function ($a, $b) {
    return strcasecmp($a['name'], $b['name']);
});

// Display results
if (!empty($results)) {
    echo "<table border='1' cellpadding='3' style='border-collapse: collapse;'>";
    foreach ($results as $venue) {
        // Create a link to details.php using the ID
        echo "<tr><td><a href=\"details.php?q={$venue['id']}\"><strong>{$venue['name']}</strong></a></td><td>{$venue['locality']}</td></tr>";
    }
    echo "</table>";
} else {
    echo "<p>No results found for \"$query\".</p>";
}
?>

