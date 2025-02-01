<?php include('header.php'); ?>

<h1>Search Results</h1>

<?php
// Get the search query from the URL
$query = isset($_GET['q']) ? strtolower(trim($_GET['q'])) : '';

if (!$query) {
    echo "<p>No query provided. Please go back and try again.</p>";
    include('footer.php');
    exit;
}

// Load the Turtle file
$file_path = 'data/linked_data_triplestore.ttl';
if (!file_exists($file_path)) {
    echo "<p>Data file not found.</p>";
    include('footer.php');
    exit;
}

// Read the Turtle file
$turtleFile = file_get_contents($file_path);

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

// Display results
if (!empty($results)) {
    echo "<ul>";
    foreach ($results as $venue) {
        // Create a link to details.php using the ID
        echo "<li><a href=\"details.php?q={$venue['id']}\"><strong>{$venue['name']}</strong></a>, {$venue['locality']}</li>";
    }
    echo "</ul>";
} else {
    echo "<p>No results found for \"$query\".</p>";
}
?>

<?php include('footer.php'); ?>
