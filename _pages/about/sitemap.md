---
title: sitemap
permalink: /map/
layout: collection
lastmod: 2022-05-09T14:35:41.594Z
tree-dir: _pages/about
tree-file: tree.txt
---

Autogenerate Site Map

[tree command](https://docs.microsoft.com/en-us/windows-server/administration/windows-commands/tree)

```powershell
# Regenerate Site Map

cd ~/github/{{ site.local_repo }}
jekyll clean
rm {{ page.tree-dir  }}/{{ page.tree-file }}
tree > {{ page.tree-dir  }}/tree-utf16.txt
Get-Content {{ page.tree-dir  }}/tree-utf16.txt -Encoding Unicode | Set-Content -Encoding UTF8 {{ page.tree-dir }}/{{ page.tree-file }}
```


```shell
# Include sitemap/tree.txt
{% include_relative {{ page.tree-file }} %}
```

