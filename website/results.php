<?php include('header.php'); ?>

<?php
// Get the search query and option from the URL
$query = isset($_GET['q']) ? strtolower(trim($_GET['q'])) : '';
$option = isset($_GET['option']) ? strtolower(trim($_GET['option'])) : '';

if (!$query || !$option) {
    echo "<p>No query or option provided. Please go back and try again.</p>";
    include('footer.php');
    exit;
}

echo "<b>Search Results: {$query}</b><br /><br />";

// Load the Turtle file
$file_path = 'data/linked_data_triplestore.ttl';
if (!file_exists($file_path)) {
    echo "<p>Data file not found.</p>";
    include('footer.php');
    exit;
}

// Read the Turtle file
$turtleFile = file_get_contents($file_path);

// Function to convert text with underscores to normal English with capitals
function convertToNormalEnglish($text) {
    return ucwords(str_replace('_', ' ', $text));
}

// Function to decode any Unicode characters in the text
function decodeUnicode($text) {
    return urldecode($text);
}

if ($option === "artist") {include "results_artist.php";}
if ($option === "venue") {include "results_venue.php";}
if ($option === "genre") {include "results_genre.php";}


?>

<?php include('footer.php'); ?>
