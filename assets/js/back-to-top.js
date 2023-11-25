//Event listener to see if scrolling has started

window.addEventListener('scroll', function() {
  var element = document.getElementById('backToTopBtn');
  var height = window.innerHeight;
  var scrollTop = document.documentElement.scrollTop || document.body.scrollTop;

  if (scrollTop > height * 0.1) { // Adjust the 0.1 to control when the opacity starts changing
      element.style.opacity = 0.2; // 20% opacity
      element.style.display = "block"
  } else {
      element.style.opacity = 0; // 0% opacity
      element.style.display = "none"
  }
});

function backToTopBtn() {
  

  
  let mybutton = document.getElementById("backToTopBtn");
 
  if (mybutton) {
    function topFunction() {
      document.body.scrollTop = 0; // For Safari
      document.documentElement.scrollTop = 0; // For Chrome, Firefox, IE and Opera
      mybutton.style.opacity = "75%";
    }
    
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
}