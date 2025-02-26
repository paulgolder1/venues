<?php
// Process the Turtle file line by line
$lines = explode("\n", $turtleFile);
$genres = [];

foreach ($lines as $line) {
    // Trim whitespace
    $line = trim($line);
    
    // Check if the line contains schema1:genre
    if (strpos($line, 'schema1:genre') !== false) {
        // Extract words starting with ex:
        preg_match_all('/ex:([a-zA-Z0-9_]+)/', $line, $matches);
        
        foreach ($matches[1] as $genre) {
            $decodedGenre = decodeUnicode(convertToNormalEnglish($genre));
            
            // Check if $query is in the genre (case-insensitive, ignoring spaces)
            if (stripos(str_replace(' ', '', $decodedGenre), str_replace(' ', '', $query)) !== false) {
                // Add to genres list if not already present
                if (!in_array($decodedGenre, $genres)) {
                    $genres[] = $decodedGenre;
                }
            }
        }
    }
}

// Sort genres alphabetically
natcasesort($genres);

// recode genres to format in Turtle file
function formatGenre($genre) {
    return strtolower(str_replace(' ', '_', $genre));
}


if (empty($genres)) {
    echo "<p>No genres found matching '$query'.</p>";
} else {
	echo "Listing genres containing <b>$query</b><br /><br />";
    echo "<ul>";
    foreach ($genres as $genre) {
		$formatted = formatGenre($genre);
        echo "<li>
        <a href='artists_in_genre.php?q=$formatted'>
        $genre
        </a>
        </li>";
    }
    echo "</ul>";
}
?>
