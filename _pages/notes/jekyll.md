---
title: Jeykll
permalink: /notes/jekyll/
lastmod: '2022-01-11T20:39:53.550Z'
---

# Jeykll

{% raw %}
[Cheatsheet](https://learn-the-web.algonquindesign.ca/topics/jekyll-cheat-sheet/)

Setup and use
Installation

All these commands should be executed in Terminal, one-by-one, in order.

```bash
xcode-select --install
/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
brew install ruby
echo 'export PATH="/usr/local/opt/ruby/bin:$PATH"' >> ~/.bash_profile
```

Then open your repo in Terminal, from GitHub Desktop: Repository > Open in Terminal

bundle init
Open the new Gemfile, add the following line:

```bash
gem "jekyll"
```

Pop back to Terminal, type:

```bash
bundle install
```

☛ Jekyll installation.

Starting & stopping

First, open your Jekyll folder in Terminal using the GitHub app shortcut—⌃`

Start Jekyll:

```bash
bundle exec jekyll serve
```

View your website in a browser:

'http://localhost:4000/'
Stop Jekyll:

Control + C
Or just quit Terminal.
☛ Jekyll terminal guide.

If hosting on GitHub, don’t forget baseurl

```bash
bundle exec jekyll serve --baseurl=""
```

Setting up Jekyll

Inside your folder you need to create the _config.yml file.

permalink: pretty

## Add the baseurl if hosting on GitHub

baseurl: /your-folder-on-github
Sample folder setup:

```bash
_config.yml
_data/
  └ dinos.yml
_includes/
  └ button.html
_layouts/
  └ default.html
_posts/
  └ 2015-10-28-new-dino.md
  └ 2015-10-25-dinos-have-feathers.md
css/
  └ main.css
images/
  └ trex.jpg
index.html
meat-eaters.html
```

Files & paths
Linking pages

With permalink: pretty turned on the .html extension can be left off URLs.

*All links & hrefs & srcs should always start with a forward slash: /

```html
<a href="/plant-eaters/">Plant eaters</a>
```

`Don’t forget to add {{site.baseurl}} when hosting on GitHub.`

`<a href="{{site.baseurl}}/plant-eaters/">Plant eaters</a>`

Connecting CSS

Link CSS files like normal, be sure to start with a /

```html
<link href="/css/main.css" rel="stylesheet">
```

Or for GitHub Pages folder hosting:

```html
<link href="{{site.baseurl}}/css/main.css" rel="stylesheet">
```

Linking images

Link images like normal, make sure to start with a /

```html
<img src="/images/trex.jpg" alt="">
```

Or for GitHub Pages folder hosting:

```html
<img src="{{site.baseurl}}/images/trex.jpg" alt="">
```

Layouts
Common header & footer

First create a new file inside the _layouts folder, name it whatever you want. Inside that file put the common
HTML.

`Use {{content}} as the placeholder for the HTML from each page.`

'_layouts/default.html'

```html
<!DOCTYPE html>
<html lang="en-ca">
<head>
  <meta charset="utf-8">
  <title></title>
</head>
<body>
  {{content}}
</body>
</html>
```

At the top of each page use YAML front matter to denote which layout to use:

index.html

```yaml
---
layout: default
---

```html
<h1>Homepage</h1>
```

Layouts can be nested by including a different layout at the top of a layout HTML file.

Page variables

To pass information from a page to a layout you can use YAML frontmatter.

`index.html`

```yaml
---
layout: default
title: Plant Eaters
---
```

Then inside the layout, we can use placeholder variables:

_layouts/default.html

```html
<!DOCTYPE html>
<html lang="en-ca">
<head>
  <meta charset="utf-8">
  <title>{{page.title}}</title>
```

⋮See the complete list of already included Jekyll page variables.

Highlighting navigation

Use an if-statement inside the `<a>` tag to add the .current class.

```html
<a href="/plant-eaters/" {% if page.url == '/plant-eaters/' %} class="current" {% endif %}>Plant eaters</a>
```

Data, includes & posts
Data

Data files allow us to separate content from it’s presentation HTML.

Put data files in the _data folder.

All the data is found in the variable site.data

 _data/dinos.yml

- name: Tyrannosaurus
  diet: Meat
  size: Big
- name: Stegosaurus
  diet: Plants
  size: Medium
- name: Velociraptor
  diet: Meat
  size: Small
Includes

Includes are for making reusable, repeatable HTML blocks.

Put includes int the _includes folder.

_includes/button.html

```html
<a class="btn" href="/go/">Go!</a>
{% include button.html %}
{% include button.html %}
```

Pass information into includes:

```html
{% include button.html url="/plant-eaters/" title="Plant eaters" %}
```

`_includes/button.html`

```html
<a class="btn" href="{{include.url}}">{{include.title}}</a>
```

Posts

Posts are like blog posts or news articles—time based, ordered content.

Posts must be inside the _posts folder.

Name posts in the following, strict format: YYYY-MM-DD-file-name.md

All the data is found in the variable site.posts

_posts/
  2013-09-26-water-in-martian-dirt.md
  2013-10-06-clouds-on-kepler-7b-mapped.md
  2013-10-09-planet-without-star.md
Use the for loop to output posts:

```html
<ul>
  {% for post in site.posts %}
    <li>
      <a href="{{post.url}}">{{post.title}}</a>
      <p>{{post.excerpt}}</p>
    </li>
  {% endfor %}
</ul>
```

Template tags
Check out the complete Liquid for Designers resource.

Output

The double curly braces, like ````{{ }}```` is to output something—they can be used anywhere to write it into the HTML.

```html
{{site.time}}
<a href="{{page.url}}">Plant eaters</a>
<h1>{{site.data.dinos[0].name}}</h1>
```

For

The for-loop is used to run over a collection of information like data or posts.

```html
{% for dino in site.data.dinos %}
  <h2>{{dino.name}}</h2>
  <dl>
    <dt>Diet</dt>
    <dd>{{site.diet}}</dd>
    <dt>Size</dt>
    <dd>{{site.size}}</dd>
  </dl>
{% endfor %}
```

If

The if-statement can be used to do different things based on certain conditions.

```html
{% if page.url == '/' %}
  <h1>Dinosaurs Rock!</h1>
{% else %}
  <strong>Dinosaurs Rock</strong>
{% endif %}
```

Template filters
Check out the complete Liquid for Designers resource & Jekyll’s filter docs.

Date

Will convert an ISO 8601 formatted date into something more friendly.

```html
{{site.time | date: '%B %-d, %Y' }}
```

Replace

Will search for all instances of a piece of text and replace it with something else.

```html
{{site.data.dinos[0].diet | replace: 'Meat', 'Plants' }}
```

Sort

Will sort a YAML object by a specific field.

```html
{{site.data.dinos | sort: 'name' }}
```

Markdownify

Takes Markdown inside YAML and converts it to HTML.

```html
    {{site.data.dinos[0].name | markdownify }}
```

Slugify

Convert text to valid classes.

```html
{{site.data.dinos[0].name | classify }}
```

Jsonify

Will convert an object or array into JSON.

```html
{{site.data.dinos | jsonify }}
```

## Auto Generate Nav

```html
<h3>Getting Started</h3>
<ul>
    {% for doc in site.docs %}
      {% if doc.category == "getting-started" %}
        <li><a href="{{ doc.url }}">{{ doc.title }}</a></li>
      {% endif %}
    {% endfor %}
</ul>
```

## Add Class or ID to markdown element

https://boringrails.com/tips/jekyll-css-class

{% endraw %}

```liquid
{% raw %}
{{site.github.repository_url}}
{% endraw %}
```

```html
{%raw %}
<div class="sidebar__top">
  <a href="'''liquid{{site.github.repository_url}}'''/blob/gh-pages/{{page.name}}">
    <i class="fab fa-github-square"></i>
  </a>
  <a href="vscode://file{{ site.local_git_pc}}/{{ site.local_repo }}/{{ page.path }}">
    <i class="fas fa-laptop-code"></i>
  </a>
  <a href="vscode://file{{ site.local_git_mac}}/{{ site.local_repo }}/{{ page.path }}">
    <i class="fas fa-laptop-code"></i>
  </a>
  <a href="#page-title" class="back-to-top">{{ site.data.ui-text[site.locale].back_to_top | default: 'Back to Top' }} &uarr;</a>
</div>
{% endraw %}
```
