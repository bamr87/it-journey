---
title: jekyll sidebar
date: 2024-05-14T20:39:28.955Z
tags: []
lastmod: 2024-05-19T16:02:26.577Z
description: null
preview: null
categories:
   - jekyll
sub-title: null
excerpt: test
snippet: null
author: null
keywords: {}
slug: jekyll-sidebar
type: posts
published: false
draft: true
---

{% raw %}

# How to Display Files and Folders in a Sidebar in Jekyll

This guide will show you how to display files and folders in a sidebar in Jekyll, and how to create a hyperlink for each file.

## Steps

1. **Get the root folder of the collection**

   In Jekyll, a collection is a group of related documents. In this case, the collection is named "notes". We use the `where` filter to find the collection with the label that matches `page.collection`, and the `first` filter to get the first (and only) match.

   ```html
   {% assign root_folder = site.collections | where: "label", page.collection | first %}
   <h2>Root Directory: {{ root_folder.label }}</h2>
   ```

2. **Sort the documents in the root folder by their path**

   Each document in a collection has a `path` property that gives its location relative to the site source. We use the `sort` filter to arrange the documents in alphabetical order by their path.

   ```html
   {% assign docs = root_folder.docs | sort: 'path' %}
   ```

3. **Initialize a variable to keep track of the previous path**

   We need to keep track of the path of the previous document so that we can compare it with the path of the current document. This allows us to determine when the path changes, which indicates a new folder.

   ```html
   {% assign prev_path = "" %}
   ```

4. **Start an unordered list to display the files and folders**

   We use an unordered list (`<ul>`) to display the files and folders. Each file and folder will be a list item (`<li>`).

   ```html
   <ul>
   ```

5. **Loop through each document**

   We use a for loop to iterate over each document in the collection.

   ```html
   {% for doc in docs %}
   ```

6. **Get the path of the current document without the file name**

   We use the `split` filter to divide the path into an array of folders, and the `pop` filter to remove the last item from the array, which is the file name. This gives us the path of the current document without the file name.

   ```html
   {% assign current_path = doc.path | split: '/' | pop %}
   ```

7. **If the current path is different from the previous path, create a new list item for each folder in the path**

   We compare the current path with the previous path. If they are different, this means we have moved to a new folder. We then create a new list item for each folder in the current path, excluding the root folder.

   ```html
   {% if current_path != prev_path %}
     {% for folder in current_path %}
       {% if forloop.index != 1 %}
         <li class="folder">{{ folder }}</li>
       {% endif %}
     {% endfor %}
     {% assign prev_path = current_path %}
   {% endif %}
   ```

8. **Create a list item with a hyperlink for each file**

   We create a list item for each file, with the file name being a hyperlink to the file's URL. We use the `doc.url` property to get the URL of the file.

   ```html
   <li class="file"><a href="{{ doc.url }}">{{ doc.title }}</a></li>
   ```

9. **End the document loop**

   We close the for loop that iterates over the documents.

   ```html
   {% endfor %}
   ```

10. **End the unordered list**

    We close the unordered list that displays the files and folders.

    ```html
    </ul>
    ```

This will display the files and folders in a sidebar, with each file being a hyperlink to its URL. The folders will not be repeated for each file, and the root folder will not be included in the path.
{% endraw %}