---
title: config
layout: default
lastmod: 2022-05-09T14:35:41.594Z
config-dir: pages/_about
config-file: _config.yml
permalink: /about/config/
---

Autogenerate Config File

[config]()

```powershell
# Regenerate Config File

cd ~/github/{{ site.local_repo }}
cp {{ page.config-file }} {{ page.config-dir  }}/config-utf16.txt
Get-Content {{ page.config-dir  }}/config-utf16.txt | Set-Content -Encoding UTF8 {{ page.config-dir }}/{{ page.config-file }}
```

```yml
# Include sitemap/config.yml
{% include_relative {{ page.config-file }} %}
```
