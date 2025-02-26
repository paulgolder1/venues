<?
// Function to parse the Turtle file and extract MusicGroup information
function parseMusicGroups($turtleFile, $query) {
    $lines = explode("\n", $turtleFile);
    $results = [];
    $currentGroup = null;
    $parsingGroup = false;
    $parsingGenres = false;
    $parsingMembers = false;
    
    foreach ($lines as $line) {
        $line = trim($line);
        
		if (preg_match('/ex:([^ ]+) a (schema1:MusicGroup|schema1:Person)/', $line, $matches)) {
            // Start a new music group
            $groupId = $matches[1];
            if (strpos($groupId, $query) !== false) {
                $parsingGroup = true;
                $currentGroup = [
                    'id' => $groupId,
                    'name' => convertToNormalEnglish(decodeUnicode($groupId)),
                    'genres' => [],
                    'members' => []
                ];
            } else {
                $parsingGroup = false;
            }
            $parsingGenres = false;
            $parsingMembers = false;
        } elseif ($parsingGroup) {
            if (strpos($line, 'schema1:genre') !== false) {
                // Start parsing genres
                $parsingGenres = true;
                $parsingMembers = false;
            } elseif (strpos($line, 'schema1:member') !== false) {
                // Start parsing members
                $parsingMembers = true;
                $parsingGenres = false;
            }
            
            if ($parsingGenres) {
                preg_match_all('/ex:([^ ,;]+)/', $line, $matches);
                foreach ($matches[1] as $genre) {
                    $currentGroup['genres'][] = convertToNormalEnglish(decodeUnicode($genre));
                }
            } elseif ($parsingMembers) {
                preg_match_all('/ex:([^ ,;]+)/', $line, $matches);
                foreach ($matches[1] as $member) {
                    $currentGroup['members'][] = convertToNormalEnglish(decodeUnicode($member));
                }
            }
            
            if (strpos($line, '.') !== false) {
                // End of the current group entry
                $results[] = $currentGroup;
                $parsingGroup = false;
                $parsingGenres = false;
                $parsingMembers = false;
            }
        }
    }
    
    // Sort results alphabetically by artist name
    usort($results, function($a, $b) {
        return strcmp($a['name'], $b['name']);
    });
    
    return $results;
}

// Parse the Turtle file to extract MusicGroup information
$results = parseMusicGroups($turtleFile, $query);

// Display results in a table
if (!empty($results)) {
    echo "<table border='1' cellpadding='3' style='border-collapse: collapse;'>";
    if (!isMobile()) {
		echo "<tr><th style='text-align: left; vertical-align: top;'>Artist</th><th style='text-align: left; vertical-align: top;'>Genre</th><th style='text-align: left; vertical-align: top;'>Members</th></tr>";
	}
    foreach ($results as $result) {
		
		if (!isMobile()) {
			echo "<tr>";
			echo "<td style='vertical-align: top;'><b>{$result['name']}</b></td>";
			echo "<td style='vertical-align: top;'>" . implode(', ', array_unique($result['genres'])) . "</td>";
			echo "<td style='vertical-align: top;'>" . implode(', ', array_unique($result['members'])) . "</td>";
			echo "</tr>";
		} else {
			echo "<tr><td colspan=3>";
			echo "<b>" . $result['name'] . "</b><br />";
			if (!empty($result['genres'])) {
				echo "<span style='color:red;'>Genres: " . implode(', ', array_unique($result['genres'])) . "</span><br />";
			}
			if (!empty($result['members'])) {
				echo "<span style='color:blue;'>Members: " . implode(', ', array_unique($result['members'])) . "</span>";
			}
			echo "</td></tr>";
		}
    }
    echo "</table>";
} else {
    echo "<p>No results found for \"$query\".</p>";
}
?>