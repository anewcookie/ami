var mySidebar = document.getElementById("mySidebar");
var overlayBg = document.getElementById("myOverlay");
var page = document.getElementById("page");

// Toggle between showing and hiding the sidebar, and add overlay effect
function w3_open() {
  mySidebar = document.getElementById("mySidebar");
  overlayBg = document.getElementById("myOverlay");
  page = document.getElementById("page");
  if (mySidebar.style.display === 'block') {
    mySidebar.style.display = 'none';
    overlayBg.style.display = "none";
    page.style.marginLeft = "0px";
  } else {
    mySidebar.style.display = 'block';
    overlayBg.style.display = "block";
    page.style.marginLeft = "300px";
  }
}

// Close the sidebar with the close button
function w3_close() {
  page = document.getElementById("page");
  mySidebar = document.getElementById("mySidebar");
  overlayBg = document.getElementById("myOverlay");
  mySidebar.style.display = "none";
  overlayBg.style.display = "none";
  page.style.marginLeft = "0px";
}
