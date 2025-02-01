<?php include('header.php'); ?>

<h1>Search</h1>

<form action="results.php" method="get">
    <label for="q">Search by Name or Locality:</label>
    <input type="text" id="q" name="q" required>
    <button type="submit">Search</button>
</form>

<?php include('footer.php'); ?>
