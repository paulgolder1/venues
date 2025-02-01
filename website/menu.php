<div class="topnav" id="myTopnav">

<?php
$url = $_SERVER['REQUEST_URI'];

<?
if ($url == "/")  {
	?><a href="/" class="active">HOME</a><?
} else { 
	?><a href="/">HOME</a><?
}
?>

<?
if ($url == "/about/")  {
	?><a href="/about/" class="active">UP</a><?
} else { 
	?><a href="/about/">UP/a><?
}
?>

<?
if ($url == "/sitemap/")  {
	?><a href="/sitemap/" class="active">DOWN<?
} else { 
	?><a href="/sitemap/">DOWN><?
}
?>

<a href="javascript:void(0);" class="icon" onclick="myFunction()">
<i class="fa fa-bars"></i>
</a>
</div>
