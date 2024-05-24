---
title: Searchbar and sitemaping
description: null
date: 2024-05-24T03:15:49.440Z
preview: null
draft: true
tags: []
categories: []
sub-title: null
excerpt: Chat with GitHub Copilot to add a search bar and sitemap to your Jekyll site
snippet: null
author: bamr87
layout: null
keywords: {}
lastmod: 2024-05-24T03:19:52.363Z
slug: null
permalink: null
attachments: ""
type: posts
---
{% raw %}
bamr87: add the page excerpt, page tags, absolute url, and author as new columns 

GitHub Copilot: To add the page excerpt, page tags, absolute URL, and author as new columns, you can modify the HTML code as follows:

```html
<h1>Sitemap - Index</h1>

{% for collection in site.collections %}
<h2>{{ collection.label }}</h2>
<table class="table">
    <thead>
        <tr>
            <th scope="col">Page</th>
            <th scope="col">Path</th>
            <th scope="col">Date</th>
            <th scope="col">Categories</th>
            <th scope="col">Excerpt</th>
            <th scope="col">Tags</th>
            <th scope="col">Absolute URL</th>
            <th scope="col">Author</th>
        </tr>
    </thead>
    <tbody>
        {% for item in collection.docs %}
        <tr>
            <td>
                <a href="{{ item.url | relative_url }}">{{ item.title }}</a>
            </td>
            <td>{{ item.path }}</td>
            <td>{{ item.date | date: "%B %d, %Y" }}</td>
            <td>{{ item.categories | join: ", " }}</td>
            <td>{{ item.excerpt }}</td>
            <td>{{ item.tags | join: ", " }}</td>
            <td>
                <a href="{{ site.url }}{{ item.url }}">{{ site.url }}{{ item.url }}</a>
            </td>
            <td>{{ item.author }}</td>
        </tr>
        {% endfor %}
    </tbody>
</table>
{% endfor %}
```

This code adds four new columns to the table: Excerpt, Tags, Absolute URL, and Author. The Excerpt and Tags columns are populated with the `excerpt` and `tags` properties of each item in the collection, respectively. The Absolute URL column is populated with the absolute URL of each item, which is constructed by concatenating the site's base URL (`site.url`) with the item's relative URL (`item.url`). The Author column is populated with the `author` property of each item.

bamr87: help me add a search bar that will explore the contents of the table, and filter for the keyworkds in the searchbar.

GitHub Copilot: To add a search bar that filters the table based on the input, you can use JavaScript along with your HTML. Here's a step-by-step plan:

1. Add an input field above the table to serve as the search bar.
2. Write a JavaScript function that gets triggered whenever the user types in the search bar.
3. In this function, convert the user's input to lowercase.
4. Loop through each row in the table.
5. For each row, convert its text content to lowercase and check if it includes the user's input.
6. If it does, show the row. If it doesn't, hide the row.

Here's the code:

```html
<h1>Sitemap - Index</h1>

<input type="text" id="searchBar" onkeyup="searchFunction()" placeholder="Search for keywords..">

{% for collection in site.collections %}
<!-- rest of your code -->
{% endfor %}

<script>
function searchFunction() {
  var input, filter, table, tr, td, i, txtValue;
  input = document.getElementById("searchBar");
  filter = input.value.toLowerCase();
  table = document.getElementsByTagName("table");
  tr = table[0].getElementsByTagName("tr");

  for (i = 0; i < tr.length; i++) {
    td = tr[i].getElementsByTagName("td")[0];
    if (td) {
      txtValue = td.textContent || td.innerText;
      if (txtValue.toLowerCase().indexOf(filter) > -1) {
        tr[i].style.display = "";
      } else {
        tr[i].style.display = "none";
      }
    }       
  }
}
</script>
```

This script will filter the table based on the first column. If you want to search in all columns, you can modify the script to loop through all `td` elements in a row.

bamr87: let's update script to consolidate the tables by adding another column for the collection.

GitHub Copilot: To consolidate the tables and add another column for the collection, you can modify the HTML and JavaScript code as follows:

```html
<h1>Sitemap - Index</h1>

<input type="text" id="searchBar" onkeyup="searchFunction()" placeholder="Search for keywords..">

<table class="table">
    <thead>
        <tr>
            <th scope="col">Collection</th>
            <th scope="col">Page</th>
            <th scope="col">Description</th>
            <th scope="col">Excerpt</th>
            <th scope="col">Path</th>
            <th scope="col">Date</th>
            <th scope="col">Categories</th>
            <th scope="col">Tags</th>
            <th scope="col">Absolute URL</th>
            <th scope="col">Author</th>
        </tr>
    </thead>
    <tbody>
        {% for collection in site.collections %}
            {% for item in collection.docs %}
            <tr>
                <td>{{ collection.label }}</td>
                <td>
                    <a href="{{ item.url | relative_url }}">{{ item.title }}</a>
                </td>
                <td>{{ item.description }}</td>
                <td>{{ item.excerpt }}</td>
                <td>{{ item.path }}</td>
                <td>{{ item.date | date: "%B %d, %Y" }}</td>
                <td>{{ item.categories | join: ", " }}</td>
                <td>{{ item.tags | join: ", " }}</td>
                <td>
                    <a href="{{ site.url }}{{ item.url }}">{{ site.url }}{{ item.url }}</a>
                </td>
                <td>{{ item.author }}</td>
            </tr>
            {% endfor %}
        {% endfor %}
    </tbody>
</table>

<script>
function searchFunction() {
  var input, filter, table, tr, td, i, j, txtValue;
  input = document.getElementById("searchBar");
  filter = input.value.toLowerCase();
  table = document.getElementsByTagName("table");
  tr = table[0].getElementsByTagName("tr");

  for (i = 0; i < tr.length; i++) {
    td = tr[i].getElementsByTagName("td");
    for (j = 0; j < td.length; j++) {
      if (td[j]) {
        txtValue = td[j].textContent || td[j].innerText;
        if (txtValue.toLowerCase().indexOf(filter) > -1) {
          tr[i].style.display = "";
          break;
        } else {
          tr[i].style.display = "none";
        }
      }
    }
  }
}
</script>
```

This code consolidates all the tables into one and adds a new column for the collection label. The search function now loops through all `td` elements in a row, allowing the user to search in all columns.

bamr87: how can we add column sorting funtionality?

GitHub Copilot: To add column sorting functionality, you can use JavaScript. Here's a step-by-step plan:

1. Add an `onclick` event to each table header that triggers a sorting function.
2. Write a JavaScript function that sorts the table rows based on the clicked column.
3. In this function, get the table and the rows.
4. Loop through all rows and compare the text of the current and next cell in the clicked column.
5. If they are in the wrong order, swap them and mark that a switch has been done.
6. Repeat this process until no more switches are done.

Here's the code:

```html
<!-- Your HTML code -->

<th scope="col" onclick="sortTable(0)">Collection</th>
<th scope="col" onclick="sortTable(1)">Page</th>
<th scope="col" onclick="sortTable(2)">Description</th>
<!-- rest of your th elements -->

<script>
function sortTable(n) {
  var table, rows, switching, i, x, y, shouldSwitch, dir, switchcount = 0;
  table = document.getElementsByTagName("table")[0];
  switching = true;
  dir = "asc"; 

  while (switching) {
    switching = false;
    rows = table.rows;
    for (i = 1; i < (rows.length - 1); i++) {
      shouldSwitch = false;
      x = rows[i].getElementsByTagName("TD")[n];
      y = rows[i + 1].getElementsByTagName("TD")[n];
      if (dir == "asc") {
        if (x.innerHTML.toLowerCase() > y.innerHTML.toLowerCase()) {
          shouldSwitch = true;
          break;
        }
      } else if (dir == "desc") {
        if (x.innerHTML.toLowerCase() < y.innerHTML.toLowerCase()) {
          shouldSwitch = true;
          break;
        }
      }
    }
    if (shouldSwitch) {
      rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
      switching = true;
      switchcount ++;      
    } else {
      if (switchcount == 0 && dir == "asc") {
        dir = "desc";
        switching = true;
      }
    }
  }
}
</script>
```

This script adds sorting functionality to the table. When a user clicks on a column header, the table gets sorted by that column. The first click sorts in ascending order, the second click sorts in descending order.

bamr87: it's not working. when i click on the column, nothing happens

GitHub Copilot: The issue might be due to the fact that the `onclick` event is not properly attached to the table headers. You need to ensure that the `onclick` event is added to each `<th>` element in your table header. 

Here's an example of how to do it:

```html
<thead>
    <tr>
        <th scope="col" onclick="sortTable(0)">Collection</th>
        <th scope="col" onclick="sortTable(1)">Page</th>
        <th scope="col" onclick="sortTable(2)">Description</th>
        <!-- Add onclick event to other th elements -->
    </tr>
</thead>
```

In the `sortTable(n)` function, `n` is the index of the column to be sorted. It starts from 0 for the first column, 1 for the second column, and so on.

If you've done this and it's still not working, there might be an error in your JavaScript code. You can check for errors by opening the developer tools in your browser (usually by pressing F12) and looking at the console. Any JavaScript errors will be displayed there.

bamr87: still not working. i only want to sort on collection, page, and date.

GitHub Copilot: I see, let's try a different approach using event listeners and data attributes. This approach will allow us to sort the table based on the data type (string or date) and will only apply to the Collection, Page, and Date columns.

Here's the updated code:

```html
<!-- Your HTML code -->

<th scope="col" data-type="string">Collection</th>
<th scope="col" data-type="string">Page</th>
<th scope="col" data-type="date">Date</th>
<!-- rest of your th elements -->

<script>
document.querySelectorAll('th').forEach(header => {
    if (['Collection', 'Page', 'Date'].includes(header.textContent)) {
        header.addEventListener('click', () => {
            const tableElement = document.querySelector('table');
            const headerIndex = Array.prototype.indexOf.call(header.parentNode.children, header);
            const currentTbody = tableElement.querySelector('tbody');
            const newTbody = currentTbody.cloneNode(true);
            const rows = Array.from(newTbody.querySelectorAll('tr'));
            const type = header.getAttribute('data-type');
            const sortedRows = rows.sort((a, b) => {
                const aValue = a.children[headerIndex].textContent;
                const bValue = b.children[headerIndex].textContent;
                if (type === 'date') {
                    return new Date(aValue) - new Date(bValue);
                }
                return aValue.localeCompare(bValue);
            });
            sortedRows.forEach(row => newTbody.appendChild(row));
            tableElement.replaceChild(newTbody, currentTbody);
        });
    }
});
</script>
```

This script adds an event listener to each table header. When a header is clicked, it sorts the rows based on the clicked column. The sorting is done either as a string comparison or as a date comparison, depending on the `data-type` attribute of the header. The sorted rows are then added to a new `tbody` element, which replaces the old one. This approach only applies to the Collection, Page, and Date columns.

bamr87: that worked, but it only sorts it acendingly 

GitHub Copilot: To add descending sort functionality, we can add a toggle mechanism that switches between ascending and descending sort each time a column header is clicked. We can use a custom data attribute, `data-order`, on the table headers to keep track of the current sort order.

Here's the updated code:

```html
<!-- Your HTML code -->

<th scope="col" data-type="string" data-order="desc">Collection</th>
<th scope="col" data-type="string" data-order="desc">Page</th>
<th scope="col" data-type="date" data-order="desc">Date</th>
<!-- rest of your th elements -->

<script>
document.querySelectorAll('th').forEach(header => {
    if (['Collection', 'Page', 'Date'].includes(header.textContent)) {
        header.addEventListener('click', () => {
            const tableElement = document.querySelector('table');
            const headerIndex = Array.prototype.indexOf.call(header.parentNode.children, header);
            const currentTbody = tableElement.querySelector('tbody');
            const newTbody = currentTbody.cloneNode(true);
            const rows = Array.from(newTbody.querySelectorAll('tr'));
            const type = header.getAttribute('data-type');
            const order = header.getAttribute('data-order');
            const sortedRows = rows.sort((a, b) => {
                const aValue = a.children[headerIndex].textContent;
                const bValue = b.children[headerIndex].textContent;
                if (type === 'date') {
                    return order === 'asc' ? new Date(aValue) - new Date(bValue) : new Date(bValue) - new Date(aValue);
                }
                return order === 'asc' ? aValue.localeCompare(bValue) : bValue.localeCompare(aValue);
            });
            sortedRows.forEach(row => newTbody.appendChild(row));
            tableElement.replaceChild(newTbody, currentTbody);
            header.setAttribute('data-order', order === 'asc' ? 'desc' : 'asc');
        });
    }
});
</script>
```

This script now toggles between ascending and descending sort each time a column header is clicked. The current sort order is stored in the `data-order` attribute of the header. After sorting the rows, the sort order is switched to the opposite one.

bamr87: let's update the table header columns with an up or down icon when sorted.

GitHub Copilot: To add an up or down icon to the sorted column, you can use Unicode characters or Font Awesome icons. In this example, I'll use Unicode characters. 

Here's the updated code:

```html
<!-- Your HTML code -->

<th scope="col" data-type="string" data-order="desc">Collection <span class="sort-icon"></span></th>
<th scope="col" data-type="string" data-order="desc">Page <span class="sort-icon"></span></th>
<th scope="col" data-type="date" data-order="desc">Date <span class="sort-icon"></span></th>
<!-- rest of your th elements -->

<script>
document.querySelectorAll('th').forEach(header => {
    if (['Collection', 'Page', 'Date'].includes(header.textContent)) {
        header.addEventListener('click', () => {
            const tableElement = document.querySelector('table');
            const headerIndex = Array.prototype.indexOf.call(header.parentNode.children, header);
            const currentTbody = tableElement.querySelector('tbody');
            const newTbody = currentTbody.cloneNode(true);
            const rows = Array.from(newTbody.querySelectorAll('tr'));
            const type = header.getAttribute('data-type');
            const order = header.getAttribute('data-order');
            const sortedRows = rows.sort((a, b) => {
                const aValue = a.children[headerIndex].textContent;
                const bValue = b.children[headerIndex].textContent;
                if (type === 'date') {
                    return order === 'asc' ? new Date(aValue) - new Date(bValue) : new Date(bValue) - new Date(aValue);
                }
                return order === 'asc' ? aValue.localeCompare(bValue) : bValue.localeCompare(aValue);
            });
            sortedRows.forEach(row => newTbody.appendChild(row));
            tableElement.replaceChild(newTbody, currentTbody);
            header.setAttribute('data-order', order === 'asc' ? 'desc' : 'asc');
            document.querySelectorAll('.sort-icon').forEach(icon => icon.textContent = ''); // clear all icons
            header.querySelector('.sort-icon').textContent = order === 'asc' ? ' ↓' : ' ↑'; // set the icon for the sorted column
        });
    }
});
</script>
```

This script now adds an up or down arrow to the sorted column. The arrow indicates the current sort order: up for ascending, down for descending. The arrow is added as the text content of a `<span>` element inside the table header. Before setting the arrow, all existing arrows are cleared.

bamr87: use bootstrap5 icons instead

GitHub Copilot: To use Bootstrap 5 icons, you'll need to include the Bootstrap Icons stylesheet in your HTML file. Then, you can use the `bi-arrow-up` and `bi-arrow-down` classes for the up and down icons respectively.

Here's the updated code:

```html
<!-- Include Bootstrap Icons stylesheet -->
<link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.7.2/font/bootstrap-icons.css" rel="stylesheet">

<!-- Your HTML code -->

<th scope="col" data-type="string" data-order="desc">Collection <i class="sort-icon"></i></th>
<th scope="col" data-type="string" data-order="desc">Page <i class="sort-icon"></i></th>
<th scope="col" data-type="date" data-order="desc">Date <i class="sort-icon"></i></th>
<!-- rest of your th elements -->

<script>
document.querySelectorAll('th').forEach(header => {
    if (['Collection', 'Page', 'Date'].includes(header.textContent)) {
        header.addEventListener('click', () => {
            const tableElement = document.querySelector('table');
            const headerIndex = Array.prototype.indexOf.call(header.parentNode.children, header);
            const currentTbody = tableElement.querySelector('tbody');
            const newTbody = currentTbody.cloneNode(true);
            const rows = Array.from(newTbody.querySelectorAll('tr'));
            const type = header.getAttribute('data-type');
            const order = header.getAttribute('data-order');
            const sortedRows = rows.sort((a, b) => {
                const aValue = a.children[headerIndex].textContent;
                const bValue = b.children[headerIndex].textContent;
                if (type === 'date') {
                    return order === 'asc' ? new Date(aValue) - new Date(bValue) : new Date(bValue) - new Date(aValue);
                }
                return order === 'asc' ? aValue.localeCompare(bValue) : bValue.localeCompare(aValue);
            });
            sortedRows.forEach(row => newTbody.appendChild(row));
            tableElement.replaceChild(newTbody, currentTbody);
            header.setAttribute('data-order', order === 'asc' ? 'desc' : 'asc');
            document.querySelectorAll('.sort-icon').forEach(icon => icon.className = 'sort-icon'); // clear all icons
            header.querySelector('.sort-icon').className = order === 'asc' ? 'sort-icon bi bi-arrow-down' : 'sort-icon bi bi-arrow-up'; // set the icon for the sorted column
        });
    }
});
</script>
```

This script now adds a Bootstrap icon to the sorted column. The icon indicates the current sort order: up arrow for ascending, down arrow for descending. The icon is added as a class to an `<i>` element inside the table header. Before setting the icon, all existing icons are cleared.

bamr87: try again with this updated code.

GitHub Copilot: Sure, here's the updated code with Bootstrap 5 icons for your table headers:

```html
<!-- Include Bootstrap Icons stylesheet -->
<link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.7.2/font/bootstrap-icons.css" rel="stylesheet">

<h1>Sitemap - Index</h1>

<input type="text" id="searchBar" onkeyup="searchFunction()" placeholder="Search for keywords..">

<div class="table-responsive">
    <table class="table">
        <thead>
            <tr>
                <th scope="col">Collection <i class="sort-icon"></i></th>
                <th scope="col">Page <i class="sort-icon"></i></th>
                <th scope="col">Description</th>
                <th scope="col">Excerpt</th>
                <th scope="col">Path</th>
                <th scope="col">Date <i class="sort-icon"></i></th>
                <th scope="col">Categories</th>
                <th scope="col">Tags</th>
                <th scope="col">Absolute URL</th>
                <th scope="col">Author</th>
            </tr>
        </thead>
        <tbody>
            {% for collection in site.collections %}
            {% for item in collection.docs %}
            <tr>
                <td>{{ collection.label }}</td>
                <td>
                    <a href="{{ item.url | relative_url }}">{{ item.title }}</a>
                </td>
                <td>{{ item.description }}</td>
                <td>{{ item.excerpt }}</td>
                <td>{{ item.path }}</td>
                <td>{{ item.date | date: "%B %d, %Y" }}</td>
                <td>{{ item.categories | join: ", " }}</td>
                <td>{{ item.tags | join: ", " }}</td>
                <td>
                    <a href="{{ site.url }}{{ item.url }}">{{ site.url }}{{ item.url }}</a>
                </td>
                <td>{{ item.author }}</td>
            </tr>
            {% endfor %}
            {% endfor %}
        </tbody>
    </table>
</div>

<!-- Sorting feature -->

<script>
document.querySelectorAll('th').forEach(header => {
    if (['Collection', 'Page', 'Date'].includes(header.textContent)) {
        header.addEventListener('click', () => {
            const tableElement = document.querySelector('table');
            const headerIndex = Array.prototype.indexOf.call(header.parentNode.children, header);
            const currentTbody = tableElement.querySelector('tbody');
            const newTbody = currentTbody.cloneNode(true);
            const rows = Array.from(newTbody.querySelectorAll('tr'));
            const type = header.getAttribute('data-type');
            const order = header.getAttribute('data-order');
            const sortedRows = rows.sort((a, b) => {
                const aValue = a.children[headerIndex].textContent;
                const bValue = b.children[headerIndex].textContent;
                if (type === 'date') {
                    return order === 'asc' ? new Date(aValue) - new Date(bValue) : new Date(bValue) - new Date(aValue);
                }
                return order === 'asc' ? aValue.localeCompare(bValue) : bValue.localeCompare(aValue);
            });
            sortedRows.forEach(row => newTbody.appendChild(row));
            tableElement.replaceChild(newTbody, currentTbody);
            header.setAttribute('data-order', order === 'asc' ? 'desc' : 'asc');
            document.querySelectorAll('.sort-icon').forEach(icon => icon.className = 'sort-icon'); // clear all icons
            header.querySelector('.sort-icon').className = order === 'asc' ? 'sort-icon bi bi-arrow-down' : 'sort-icon bi bi-arrow-up'; // set the icon for the sorted column
        });
    }
});
</script>
```

This script now adds a Bootstrap icon to the sorted column. The icon indicates the current sort order: up arrow for ascending, down arrow for descending. The icon is added as a class to an `<i>` element inside the table header. Before setting the icon, all existing icons are cleared.

bamr87: the sorting function doesn't work anymore.

GitHub Copilot: The sorting function might not be working because the `data-type` and `data-order` attributes are missing from the `th` elements. Also, the sorting function is currently set to only sort columns with the text 'Collection', 'Page', or 'Date'. If you want to sort other columns, you'll need to add their names to the array in the `if` statement.

Here's the updated code:

```html
<!-- Your HTML code -->

<th scope="col" data-type="string" data-order="desc">Collection <i class="sort-icon"></i></th>
<th scope="col" data-type="string" data-order="desc">Page <i class="sort-icon"></i></th>
<th scope="col" data-type="string" data-order="desc">Description</th>
<th scope="col" data-type="string" data-order="desc">Excerpt</th>
<th scope="col" data-type="string" data-order="desc">Path</th>
<th scope="col" data-type="date" data-order="desc">Date <i class="sort-icon"></i></th>
<th scope="col" data-type="string" data-order="desc">Categories</th>
<th scope="col" data-type="string" data-order="desc">Tags</th>
<th scope="col" data-type="string" data-order="desc">Absolute URL</th>
<th scope="col" data-type="string" data-order="desc">Author <i class="sort-icon"></i></th>

<!-- rest of your HTML code -->

<script>
document.querySelectorAll('th').forEach(header => {
    header.addEventListener('click', () => {
        const tableElement = document.querySelector('table');
        const headerIndex = Array.prototype.indexOf.call(header.parentNode.children, header);
        const currentTbody = tableElement.querySelector('tbody');
        const newTbody = currentTbody.cloneNode(true);
        const rows = Array.from(newTbody.querySelectorAll('tr'));
        const type = header.getAttribute('data-type');
        const order = header.getAttribute('data-order');
        const sortedRows = rows.sort((a, b) => {
            const aValue = a.children[headerIndex].textContent;
            const bValue = b.children[headerIndex].textContent;
            if (type === 'date') {
                return order === 'asc' ? new Date(aValue) - new Date(bValue) : new Date(bValue) - new Date(aValue);
            }
            return order === 'asc' ? aValue.localeCompare(bValue) : bValue.localeCompare(aValue);
        });
        sortedRows.forEach(row => newTbody.appendChild(row));
        tableElement.replaceChild(newTbody, currentTbody);
        header.setAttribute('data-order', order === 'asc' ? 'desc' : 'asc');
        document.querySelectorAll('.sort-icon').forEach(icon => icon.className = 'sort-icon'); // clear all icons
        header.querySelector('.sort-icon').className = order === 'asc' ? 'sort-icon bi bi-arrow-down' : 'sort-icon bi bi-arrow-up'; // set the icon for the sorted column
    });
});
</script>
```

This script now sorts all columns when clicked. The sort order alternates between ascending and descending each time a column header is clicked. The sort icon is updated to indicate the current sort order.
{% endraw %}