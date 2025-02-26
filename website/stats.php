<?php include ('header.php') ?>

<h1>Statistics</h1>

<?php

// Display all errors
ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);
error_reporting(E_ALL);

function countSchemas($filename) {
    // Initialize an array to hold the schema types
    $schemas = [];
    $lineCount = 0;

    // Open the file for reading
    if (($handle = fopen($filename, "r")) !== FALSE) {
        // Loop through each line of the file
        while (($line = fgets($handle)) !== FALSE) {
            $lineCount++;
            // Check if the line contains a schema type
            if (preg_match('/a schema1:(\w+) ;/', $line, $matches)) {
                $schema = $matches[1];
                // Add the schema to the array if it's not already there
                if (!isset($schemas[$schema])) {
                    $schemas[$schema] = 0;
                }
                $schemas[$schema]++;
            }
        }
        // Close the file handle
        fclose($handle);
    } else {
        echo "Error: Could not open file $filename.<br>";
    }

    return [$schemas, $lineCount];
}

// Start timing
$startTime = microtime(true);

// Open file and count schemas
$filename = __DIR__ . '/data/linked_data_triplestore.ttl';
list($schemas, $lineCount) = countSchemas($filename);

// End timing
$endTime = microtime(true);
$executionTime = $endTime - $startTime;

echo "<b>Triplestore processing</b><br /><br />The triplestore has " . number_format($lineCount) . " lines.<br />";
echo "The countSchemas function took " . number_format($executionTime, 2) . " seconds to process.<br /><br />";

echo "<b>Schemas</b><br /><br />There are " . count($schemas) . " different schemas in the triplestore.<br /><br />";

// Calculate total count
$totalCount = array_sum($schemas);

echo "<table border='1' style='border-collapse: collapse;'>";
echo "<tr><th style='padding: 5px;'>Schema</th><th style='text-align: right; padding: 5px;'>Count</th></tr>";
foreach ($schemas as $schema => $count) {
    echo "<tr><td style='padding: 5px;'>" . htmlspecialchars($schema ?? '') . "</td><td style='text-align: right; padding: 5px;'>" . htmlspecialchars(number_format($count ?? 0)) . "</td></tr>";
}
echo "<tr><td style='padding: 5px;'><strong>Total</strong></td><td style='text-align: right; padding: 5px;'><strong>" . htmlspecialchars(number_format($totalCount ?? 0)) . "</strong></td></tr>";
echo "</table>";

?>

<?php include ('footer.php') ?>