document.addEventListener('DOMContentLoaded', (event) => {
  let mybutton = document.getElementById("backToTopBtn");

  function topFunction() {
    document.body.scrollTop = 0; // For Safari
    document.documentElement.scrollTop = 0; // For Chrome, Firefox, IE and Opera
    mybutton.style.opacity = "75%";
  }

  if (mybutton) {
    mybutton.onclick = topFunction;
  }

  // When the user scrolls down 20px from the top of the document, show the button
  window.onscroll = function() {scrollFunction()};

  function scrollFunction() {
    if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
      mybutton.style.display = "block";
    } else {
      mybutton.style.display = "none";
    }
  }
});
