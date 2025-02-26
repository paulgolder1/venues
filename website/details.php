<?php include('header.php'); ?>

<h1>Search Results</h1>

<?php

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

// Function to format performer names and decode from Unicode
function formatPerformerName($performer) {
    // Remove the 'ex:' prefix and replace underscores with spaces
    $name = str_replace('ex:', '', $performer);
    $name = str_replace('_', ' ', $name);
    // Decode URL-encoded characters
    $name = urldecode($name);
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

// Define the regex pattern to capture venue details with the given ID
$pattern = '/ex:([a-z0-9]+) a schema1:MusicVenue ;\s+schema1:addressLocality "([^"]+)" ;\s+schema1:geo "([^"]+)" ;\s+schema1:name "([^"]+)" ./';

// Apply the regex to find all matches
preg_match_all($pattern, $content, $matches, PREG_SET_ORDER);

// Iterate through the matches
$venueDetails = null;
foreach ($matches as $match) {
    // The match[1] is the ID (without "ex:")
    $venueId = $match[1];
    $addressLocality = $match[2];
    $geo = $match[3];
    $name = $match[4];

    // Check if the venue ID matches the query
    if ($venueId === $query) {
        // If match found, store the venue details
        $venueDetails = [
            'name' => $name,
            'location' => $addressLocality,
            'geo' => $geo,
        ];
        break; // Stop after finding the first match
    }
}

// Output the results
if ($venueDetails) {
	echo "Here is a list of concerts taking place in <b>" .htmlspecialchars($venueDetails['name']) . ", " . htmlspecialchars($venueDetails['location']) . "</b><br /><br />";
} else {
    echo "<p>Venue not found for ID: " . htmlspecialchars($query) . "</p>";
}

// Extract performers and performance dates
$performersAndDates = extractPerformersAndDates($content, $query);

// Check if we have any performances
if (empty($performersAndDates)) {
    echo "No performances found for the provided query.";
    exit;
}

// Sort the performances by date (most recent first)
usort($performersAndDates, function($a, $b) {
    // Convert the date from string to timestamp for comparison
    $dateA = DateTime::createFromFormat('d-m-Y', $a[1])->getTimestamp();
    $dateB = DateTime::createFromFormat('d-m-Y', $b[1])->getTimestamp();
    return $dateB - $dateA; // For descending order
});

// Prepare the output
$output = "<table border='1' cellpadding='3' style='border-collapse: collapse;'>";
if (!isMobile()) {
		$output .= '<tr><th>Date</th><th>Artist</th><th>Genres</th></tr>';
}
		
foreach ($performersAndDates as $match) {
    $date = $match[1];
    $performer = $match[2];
    $performer = rtrim($performer, ",\r\n"); // Remove trailing comma and carriage return/newline if present
	$encoded_performer = preg_replace('/^ex:/', '', $performer);
    $genres = extractGenres($content, $performer);
    $genresString = implode(', ', $genres);
    $genresString = str_replace('_', ' ', $genresString); // Replace underscores with spaces
    $formattedPerformer = formatPerformerName($performer);
    
    // Add inline style to ensure all cells align to the top and prevent wrapping
    if (!isMobile()) {
		$output .= '<tr>
			<td style="padding-right:30px; white-space: nowrap; vertical-align: top;">' . $date . '</td>
			<td style="padding-right:30px; vertical-align: top;">' . '<a href="results.php?q=' . $encoded_performer . '&option=artist">' . $formattedPerformer . '</a></td>
			<td style="vertical-align: top;">' . $genresString . '</td>
		</tr>';
	} else {
		if ($genresString == "") {$genresString = "No genre listed so far";}
		$output .= '<tr>
			<td colspan="3" style="vertical-align: top;">' . $date . '<br /><b>' . '<a href="results.php?q=' . $encoded_performer . '&option=artist">' . $formattedPerformer . '</a></b><br />' . $genresString . '</td>
		</tr>';	
	}
	
}
$output .= '</table>';

// Output the results
echo $output;
?>

<?php include('footer.php'); ?>