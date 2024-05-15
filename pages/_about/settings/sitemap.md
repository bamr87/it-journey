---
title: sitemaps
lastmod: 2024-05-15T02:15:03.067Z
tree-dir: _about
tree-file: tree.txt
---

{{page.collection}}

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

```shell
#!/bin/bash

# Navigate to the repository
cd ~/github/{{ site.local_repo }}

# Clean the Jekyll site
jekyll clean

# Remove the old tree file
rm {{ page.tree-dir  }}/{{ page.tree-file }}

# Generate the new tree file
tree > {{ page.tree-dir  }}/tree-utf16.txt

# Convert the encoding of the tree file
Get-Content {{ page.tree-dir  }}/tree-utf16.txt -Encoding Unicode | Set-Content -Encoding UTF8 {{ page.tree-dir }}/{{ page.tree-file }}

# Build the Jekyll site
jekyll build

```

{% include sitemap.html %}