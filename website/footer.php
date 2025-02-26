



</div>

</div>
</div>

<div class="footer">
&copy; P. Golder, 2025.
</div>

</div>

<script>
  // Function to adjust font size
  function adjustFontSize(direction) {
    // Select the mainPanel class
    const mainPanel = document.querySelector('.mainPanel');
    if (mainPanel) {
      // Get the current font size
      const currentFontSize = parseFloat(window.getComputedStyle(mainPanel).fontSize);
      const change = direction === 'increase' ? 2 : -2;
      const newFontSize = Math.max(currentFontSize + change, 10); // Set a minimum font size (10px)
      mainPanel.style.fontSize = `${newFontSize}px`;
    }
  }
</script>


<script>
function myFunction() {
  var x = document.getElementById("myTopnav");
  if (x.className === "topnav") {
    x.className += " responsive";
  } else {
    x.className = "topnav";
  }
}
</script>

</body>
</html>