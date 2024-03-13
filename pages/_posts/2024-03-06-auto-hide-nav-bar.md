---
title: Auto Hide Navbar
description: How to update the navbar HTML file to automatically hide while scrolling down and reappear when scrolling up.
author: Github Copilot
excerpt: "To achieve this, you will need to use JavaScript along with CSS. Here's a step-by-step plan:"
date: 2019-08-22T15:20:28.000Z
lastmod: 2024-03-06T23:56:19.751Z
draft: true
tags:
    - feature
categories: []
meta: null
snippet: null
slug: auto-hide-navbar
---

# Auto Hide Navbar

How to update the navbar HTML file to automatically hide while scrolling down and reappear when scrolling up.

## Question

bamr87: how do i update the navbar html file to automatically hide while scrolling down and reappear when scrolling up?

## Answer

GitHub Copilot: To achieve this, you will need to use JavaScript along with CSS. Here's a step-by-step plan:

1. Add a unique ID to the navbar in your HTML file.
2. Create a CSS class that will hide the navbar.
3. Write a JavaScript function that will add or remove the CSS class based on the scroll direction.

Here's the code:

**HTML:**
```html
<!-- Add an ID to the navbar -->
<nav id="navbar">
    <!-- Your existing navbar code -->
</nav>
```

**CSS:**
```css
/* Add this to your CSS file */
.hide-navbar {
    top: -100px;
    transition: top 0.3s;
}
```

**JavaScript:**
```javascript
// Add this to your JavaScript file
let lastScrollTop = 0;
const navbar = document.getElementById('navbar');

window.addEventListener('scroll', function() {
    let scrollTop = window.pageYOffset || document.documentElement.scrollTop;
    if (scrollTop > lastScrollTop) {
        navbar.classList.add('hide-navbar');
    } else {
        navbar.classList.remove('hide-navbar');
    }
    lastScrollTop = scrollTop;
});
```

This JavaScript code listens for the scroll event. When the user scrolls down (i.e., the current scroll position is greater than the last scroll position), the `hide-navbar` class is added to the navbar, hiding it. When the user scrolls up, the `hide-navbar` class is removed, making the navbar visible again.

## Issue 1: Error in the Browser

bamr87: i'm receiving an error in the browser saying "Uncaught TypeError: Cannot read properties of null (reading 'classList')"

## Answer: Fixing the Error

GitHub Copilot: The error message "Uncaught TypeError: Cannot read properties of null (reading 'classList')" typically means that the JavaScript is trying to access an element that doesn't exist or hasn't been created yet.

In your case, it seems like the JavaScript code is trying to access the navbar element before it has been loaded. This can happen if your JavaScript code is placed in the `<head>` of your HTML document, or before the navbar element in the body of your HTML document.

To fix this, you can either:

1. Move your JavaScript code to the end of the body of your HTML document, just before the closing `</body>` tag. This ensures that the DOM is fully loaded before your JavaScript tries to access any elements.

2. Or, you can wrap your JavaScript code in a `window.onload` or `document.addEventListener('DOMContentLoaded', function() {...})` event to ensure that your code only runs after the entire HTML document has been fully loaded.

Here's how you can do the second option:

```javascript
window.onload = function() {
    let lastScrollTop = 0;
    const navbar = document.getElementById('navbar');

    window.addEventListener('scroll', function() {
        let scrollTop = window.pageYOffset || document.documentElement.scrollTop;
        if (scrollTop > lastScrollTop) {
            navbar.classList.add('hide-navbar');
        } else {
            navbar.classList.remove('hide-navbar');
        }
        lastScrollTop = scrollTop;
    });
}
```

Also, make sure that the ID of your navbar in your HTML matches the ID used in your JavaScript. In this case, both should be 'navbar'.

bamr87: The navbar is still fixed at the top.

GitHub Copilot: The navbar is still fixed at the top because the CSS class `hide-navbar` is not effectively hiding the navbar. The `top: -100px;` style may not work if the navbar is positioned fixed or sticky, as it seems to be in your case (since you have the `sticky-top` class applied).

Instead, you can use `transform: translateY(-100%);` to move the navbar out of view. This will move the navbar up by its own height, effectively hiding it.

Here's the updated CSS:

```css
.hide-navbar {
    transform: translateY(-100%);
    transition: transform 0.3s;
}
```

And the JavaScript remains the same:

```javascript
window.onload = function() {
    let lastScrollTop = 0;
    const navbar = document.getElementById('navbar');

    window.addEventListener('scroll', function() {
        let scrollTop = window.pageYOffset || document.documentElement.scrollTop;
        if (scrollTop > lastScrollTop) {
            navbar.classList.add('hide-navbar');
        } else {
            navbar.classList.remove('hide-navbar');
        }
        lastScrollTop = scrollTop;
    });
}
```

This should hide the navbar when scrolling down and show it when scrolling up.

## Enhancement: Smooth Transition

bamr87: ok it works now, however, when i scroll back up, i would like the navbar to transistion into view instead of instantly appearing.

## Answer: Adding a Transition

GitHub Copilot: Great! To make the navbar transition into view when scrolling up, you need to add a transition property to the original navbar style, not just the `.hide-navbar` class. This will ensure that the transition is applied both when the class is added and when it is removed.

Here's how you can do it:

**CSS:**
```css
#navbar {
    transition: transform 0.3s;
}

.hide-navbar {
    transform: translateY(-100%);
}
```

This CSS code will apply a transition to the `transform` property of the navbar, making it slide smoothly into and out of view when scrolling.

The JavaScript code remains the same:

```javascript
window.onload = function() {
    let lastScrollTop = 0;
    const navbar = document.getElementById('navbar');

    window.addEventListener('scroll', function() {
        let scrollTop = window.pageYOffset || document.documentElement.scrollTop;
        if (scrollTop > lastScrollTop) {
            navbar.classList.add('hide-navbar');
        } else {
            navbar.classList.remove('hide-navbar');
        }
        lastScrollTop = scrollTop;
    });
}
```

This should give you a smooth transition when scrolling up and down.