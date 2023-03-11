---
title: Add Floating Back-to-Top button
description: "How to Add a floating button that will scroll to the top of a page? "
date: 2023-03-09T00:15:05.278Z
preview: ""
tags: Bootstrap
categories: How-To
sub-title: ""
author: ""
excerpt: ""
snippet: ""
lastmod: 2023-03-11T18:03:19.840Z
---

[w3 schools](https://www.w3schools.com/howto/howto_js_scroll_to_top.asp)

## How To Create a Scroll To Top Button
------------------------------------

### Step 1) Add HTML:

Create a button that will take the user to the top of the page when clicked on:

```html
<!-- Sidebar-right.html  -->
<!-- Back to Top -->
  <button onclick="backToTopBtn()" id="backToTopBtn" title="Go to top" class="btn btn-primary">{{ site.data.ui-text[site.locale].back_to_top | default: 'Back to Top' }} &uarr;
  </button>
```
#### Step 2) Add CSS:

Style the button:

```scss
// Floating back to top button

#backToTopBtn { 
    display: block; /* Hidden by default */
    position: fixed; /* Fixed/sticky position */
    bottom: 20px; /* Place the button at the bottom of the page */
    right: 30px; /* Place the button 30px from the right */
    z-index: 99; /* Make sure it does not overlap */
    border: none; /* Remove borders */
    outline: none; /* Remove outline */
    background-color: $primary; /* Set a background color */
    color: inherit; /* Text color */
    opacity: 50%;
    cursor: pointer; /* Add a mouse pointer on hover */
    padding: 15px; /* Some padding */
    border-radius:10px;/* Rounded corners */
    font-size:18px;/* Increase font size */
  }
    
  #backToTopBtn:hover { 
    background-color: #555; /* Add a dark-grey background on hover */ 
    opacity: 100%;
  }
```

### Add the JavaScript

```js
// assets/js/back-to-top.js

function backToTopBtn () {
  topFunction();   

  let mybutton = document.getElementById("backToTopBtn");
  // When the user scrolls down 20px from the top of the document, show the button
  window.onscroll = function() {scrollFunction()};
  
  function scrollFunction() {
    if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
      mybutton.style.display = "block";
    } else {
      mybutton.style.display = "none";
    }
  }
  
  // When the user clicks on the button, scroll to the top of the document
  mybutton.onclick = function() {topFunction()};
  
  function topFunction() {
    document.body.scrollTop = 0; // For Safari
    document.documentElement.scrollTop = 0; // For Chrome, Firefox, IE and Opera
  }
}
```

### Add the JS source to head

```html
<!-- includes/head.html -->

<!-- Custom JS Scripts -->

<script src="/assets/js/back-to-top.js"></script>

```

