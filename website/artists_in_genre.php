<?php include('header.php'); ?>

<?php
// Get the genre query from the URL
$query = isset($_GET['q']) ? strtolower(trim($_GET['q'])) : '';
if (!$query) {
    echo "<p>No genre provided. Please go back and try again.</p>";
    exit;
}

// Load the Turtle file
$file_path = 'data/linked_data_triplestore.ttl';
if (!file_exists($file_path)) {
    echo "<p>Data file not found.</p>";
    exit;
}

$turtleFile = file_get_contents($file_path);

// Define a function to decode artist names (capitalize each word and replace underscores with spaces)
function decodeArtistName($name) {
    $name = str_replace('_', ' ', $name);  // Replace underscores with spaces
    return ucwords($name);  // Capitalize each word
}

// Initialize the artists array
$artists = [];

// Split the file content by periods to process each block
$chunks = explode('.', $turtleFile);

foreach ($chunks as $chunk) {
    // Look for artist names, which are found before "a schema1:MusicGroup" or "a schema1:Person"
    if (preg_match('/ex:(\w+)\s+a\s+schema1:(MusicGroup|Person)/i', $chunk, $matches)) {
        // Extract the artist name (e.g., "blur" from "ex:blur")
        $artistName = $matches[1];

        // Now check if the genre (ex:$query) appears before the next period in the file
        if (strpos($chunk, 'ex:' . $query) !== false) {
            // If genre matches, add the artist to the list
            $artists[] = decodeArtistName($artistName);
        }
    }
}

// Remove duplicates from the $artists array
$artists = array_unique($artists);

// Sort the artists alphabetically
sort($artists);

// Display the results
if (!empty($artists)) {
    echo "<b>Artists in the genre " . ucfirst(str_replace('_', ' ', $query)) . "</b><br /><br />";
    echo "<ul>";
    foreach ($artists as $artist) {
        echo "<li>" . htmlspecialchars($artist) . "</li>";
    }
    echo "</ul>";
} else {
    echo "<p>No artists found in this genre.</p>";
}

?>

<?php include('footer.php'); ?>
