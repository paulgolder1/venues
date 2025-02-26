<div class="topnav" id="myTopnav">

<?php

// get name of current file
$url = $_SERVER['REQUEST_URI'];

// create conditional sets to highlight page on menu if we are at that page
if ($url == "/")  {
	?><a href="index.php" class="active">HOME</a><?
} else { 
	?><a href="index.php">HOME</a><?
}

if ($url == "near_me.php")  {
	?><a href="near_me.php" class="active">WHAT'S NEAR ME?</a><?
} else { 
	?><a href="near_me.php">WHAT'S NEAR ME?</a><?
}

if ($url == "search.php")  {
	?><a href="search.php" class="active">SEARCH</a><?
} else { 
	?><a href="search.php">SEARCH</a><?
}

if ($url == "stats.php")  {
	?><a href="stats.php class="active">STATS</a><?
} else { 
	?><a href="stats.php">STATS</a><?
}

?>

<!--- javascript to change size of font across the website --->
<a href="javascript:void(0);" onclick="adjustFontSize('increase')">FONT SIZE &uarr;</a>
<a href="javascript:void(0);" onclick="adjustFontSize('decrease')">FONT SIZE &darr;</a>

<a href="javascript:void(0);" class="icon" onclick="myFunction()">
<i class="fa fa-bars"></i>
</a>
</div>
