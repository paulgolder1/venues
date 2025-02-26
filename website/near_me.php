<?php include('header.php'); ?>

<h1>What's near me?</h1>

<form action="near_me_results.php" method="get">
    <label for="q">Enter postcode:</label>
    <input type="text" id="q" name="q" required>
    
    
    <button type="submit">Search</button>
</form>

<?php include('footer.php'); ?>