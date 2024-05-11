---
title: sitemaps
lastmod: 2024-05-11T22:59:05.897Z
tree-dir: _about
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

