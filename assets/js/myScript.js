function myFunction() {
    myVar = 1;
    myVar = myVar + 1;
    document.getElementById("demo").innerHTML = myVar;
  }

// Updates each img tag with the class img-fluid

  var imgs = document.getElementsByTagName('img');
  for (var i = 0; i < imgs.length; i++) {
    imgs[i].classList.add('img-fluid');
  }
  