<?php include('header.php'); ?>

<h1>Search</h1>

<form action="results.php" method="get">
    <label for="q">Search:</label>
    <input type="text" id="q" name="q" required>
    
    <p>Choose one:</p>
    
    <label>
        <input type="radio" name="option" value="venue" required checked>
        Venue
    </label><br>
    
    <label>
        <input type="radio" name="option" value="artist" required>
        Artist
    </label><br>
    
    <label>
        <input type="radio" name="option" value="genre" required>
        Genre
    </label><br><br>
    
    <button type="submit">Search</button>
</form>

<?php include('footer.php'); ?>