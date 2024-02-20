---
title: Jekyll Setup
author: null
layout: default
description: null
categories:
  - quickstart
slug: jekyll
lastmod: 2023-11-20T04:55:27.266Z
draft: false
---

Jekyll is a static site generator. It takes text written in your
favorite markup language and uses layouts to create a static website. You can
tweak the site's look and feel, URLs, the data displayed on the page, and more. 

## Prerequisites

Jekyll requires the following:

* Ruby version **{{ site.data.ruby.min_version }}** or higher
* RubyGems
* GCC and Make

If you want to use Github Pages, here are the [dependencies](https://pages.github.com/versions.json) 



## Instructions

1. Create a new Jekyll site at `./mysite`.

```
cd ~/github/
jekyll new mysite
```

4. Change into your new directory.
```
cd mysite
```
5. Build the site and make it available on a local server.
```
bundle exec jekyll serve
```
6. Browse to [http://localhost:4000](http://localhost:4000){:target="_blank"}

{: .note .warning}
If you are using Ruby version 3.0.0 or higher, step 5 [may fail](https://github.com/github/pages-gem/issues/752). You may fix it by adding `webrick` to your dependencies: `bundle add webrick`

{: .note .info}
Pass the `--livereload` option to `serve` to automatically refresh the page with each change you make to the source files: `bundle exec jekyll serve --livereload`


If you encounter any errors during this process, check that you have installed all the prerequisites in [Requirements]({{ '/docs/installation/#requirements' | relative_url }}). 
If you still have issues, see [Troubleshooting]({{ '/docs/troubleshooting/#configuration-problems' | relative_url }}).

{: .note .info}
Installation varies based on your operating system. See our [guides]({{ '/docs/installation/#guides' | relative_url }}) for OS-specific instructions.
