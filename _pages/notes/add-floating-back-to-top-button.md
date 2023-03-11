---
title: Add Floating Back-to-Top button
description: ""
date: 2023-03-09T00:15:05.278Z
preview: ""
tags: ""
categories: ""
sub-title: ""
author: ""
excerpt: ""
snippet: ""
lastmod: 2023-03-09T03:14:23.426Z
---

[w3 schools](https://www.w3schools.com/howto/howto_js_scroll_to_top.asp)

How To Create a Scroll To Top Button
------------------------------------

##### Step 1) Add HTML:

Create a button that will take the user to the top of the page when clicked on:

### Example

<button onclick="topFunction()" id="myBtn" title="Go to top">Top</button>

* * * * *

##### Step 2) Add CSS:

Style the button:

### Example

#myBtn { display: none; /* Hidden by default */
  position: fixed; /* Fixed/sticky position */
  bottom: 20px; /* Place the button at the bottom of the page */
  right: 30px; /* Place the button 30px from the right */
  z-index: 99; /* Make sure it does not overlap */
  border: none; /* Remove borders */
  outline: none; /* Remove outline */
  background-color: red; /* Set a background color */
  color: white; /* Text color */
  cursor: pointer; /* Add a mouse pointer on hover */
  padding: 15px; /* Some padding */
  border-radius: 10px; /* Rounded corners */
  font-size: 18px; /* Increase font size */ }

#myBtn:hover { background-color: #555; /* Add a dark-grey background on hover */ }How To Create a Scroll To Top Button
------------------------------------

##### Step 1) Add HTML:

Create a button that will take the user to the top of the page when clicked on:

### Example

<button onclick="topFunction()" id="myBtn" title="Go to top">Top</button>

* * * * *

##### Step 2) Add CSS:

Style the button:

### Example

#myBtn { display: none; /* Hidden by default */
  position: fixed; /* Fixed/sticky position */
  bottom: 20px; /* Place the button at the bottom of the page */
  right: 30px; /* Place the button 30px from the right */
  z-index: 99; /* Make sure it does not overlap */
  border: none; /* Remove borders */
  outline: none; /* Remove outline */
  background-color: red; /* Set a background color */
  color: white; /* Text color */
  cursor: pointer; /* Add a mouse pointer on hover */
  padding: 15px; /* Some padding */
  border-radius: 10px; /* Rounded corners */
  font-size: 18px; /* Increase font size */ }

#myBtn:hover { background-color: #555; /* Add a dark-grey background on hover */ }