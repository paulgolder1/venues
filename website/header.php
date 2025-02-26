<!DOCTYPE html>
<html>
<head>

<?
// Display all errors
ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);
error_reporting(E_ALL);

function isMobile() {
    return preg_match('/(android|iphone|ipad|ipod|blackberry|opera mini|windows phone|iemobile|mobile)/i', $_SERVER['HTTP_USER_AGENT']);
}
?>

<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta charset="UTF-8">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fredoka+One&family=Lato&family=Rokkitt&display=swap" rel="stylesheet">
<link rel="stylesheet" href="style.css" type="text/css" media="all" />

<link rel="apple-touch-icon" sizes="76x76" href="/favicon/apple-touch-icon.png">
<link rel="icon" type="image/png" sizes="32x32" href="/favicon/favicon-32x32.png">
<link rel="icon" type="image/png" sizes="16x16" href="/favicon/favicon-16x16.png">
<link rel="manifest" href="/favicon/site.webmanifest">
<link rel="mask-icon" href="/favicon/safari-pinned-tab.svg" color="#5bbad5">
<meta name="msapplication-TileColor" content="#da532c">
<meta name="theme-color" content="#ffffff">

<title>The Venues Project</title>


</head>
<body>

<div class="wholeArea">
    
    <div class="header">
	<img src="images/tvp.jpg">
    </div>
    

<? include "menu.php"; ?>

    
<div class="mainPanel">
<div class="row">
<div class="rm20">