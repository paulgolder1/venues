<?php include('header.php'); ?>

<h1>Search Results</h1>

<?php
// details.php

// Function to extract performers and performance dates
function extractPerformersAndDates($content, $query) {
    $pattern = '/ex:show_' . preg_quote($query) . '_\d{2}-\d{2}-\d{4} a schema1:Event ;\s*schema1:location ex:' . preg_quote($query) . ' ;\s*schema1:performanceDate "(\d{2}-\d{2}-\d{4})" ;\s*schema1:performer (ex:[^ ]*) ./';
    preg_match_all($pattern, $content, $matches, PREG_SET_ORDER);
    return $matches;
}

// Function to extract genres for a performer
function extractGenres($content, $performer) {
    // Search for the performer entry in the content
    $startPos = strpos($content, $performer . ' a schema1:MusicGroup');
    if ($startPos === false) {
        return [];
    }

    // Extract the segment of text starting from the performer entry
    $performerText = substr($content, $startPos);

    // Find the end of the performer's description (indicated by a period)
    $endPos = strpos($performerText, '.');
    if ($endPos === false) {
        return [];
    }

    // Extract the relevant segment of text
    $performerText = substr($performerText, 0, $endPos + 1);

    // Extract genres from the text
    $genrePattern = '/schema1:genre\s+([^;.]+)[;.]?/';
    preg_match($genrePattern, $performerText, $genreMatch);
    if (isset($genreMatch[1])) {
        $genreText = $genreMatch[1];
        $genres = array_map('trim', explode(',', $genreText));
        // Clean up the genre names
        $genres = array_map(function($genre) {
            return str_replace('ex:', '', $genre);
        }, $genres);
        return $genres;
    }
    return [];
}

// Function to format performer names
function formatPerformerName($performer) {
    // Remove the 'ex:' prefix and replace underscores with spaces
    $name = str_replace('ex:', '', $performer);
    $name = str_replace('_', ' ', $name);
    // Capitalize each word
    $name = ucwords($name);
    return $name;
}

// Get the query parameter
$query = isset($_GET['q']) ? $_GET['q'] : '';

if (!$query) {
    echo "Query parameter 'q' is missing.";
    exit;
}

// Read the TTL file
$ttlFile = 'data/linked_data_triplestore.ttl'; 
$content = file_get_contents($ttlFile);

if ($content === false) {
    echo "Error reading TTL file.";
    exit;
}

// Extract performers and performance dates
$performersAndDates = extractPerformersAndDates($content, $query);

// Check if we have any performances
if (empty($performersAndDates)) {
    echo "No performances found for the provided query.";
    exit;
}

// Prepare the output
$output = '<table><tr><th>Date</th><th>Artist</th><th>Genres</th></tr>';
foreach ($performersAndDates as $match) {
    $date = $match[1];
	$performer = $match[2];
	$performer = rtrim($performer, ",\r\n"); // Remove trailing comma and carriage return/newline if present
    $genres = extractGenres($content, $performer);
    $genresString = implode(', ', $genres);
    $genresString = str_replace('_', ' ', $genresString); // Replace underscores with spaces
    $formattedPerformer = formatPerformerName($performer);
	$output .= '<tr><td style="padding-right:30px;">' . $date . '</td><td style="padding-right:30px;">' . $formattedPerformer . '</td><td>' . $genresString . '</td></tr>';
}
$output .= '</table>';

// Output the results within HTML
echo $output;
?>

<?php include('footer.php'); ?>