---
title: Jekyll Configuration
excerpt: Configuration file contents and regeneration steps.
lastmod: 2024-05-31T01:57:04.547Z
config-dir: pages/_about/settings
config-file: _config.yml
permalink: /about/config/
---

## Regenerate Config File with PowerShell

```powershell
# Regenerate Config File

cd ~/github/{{ site.local_repo }}
cp {{ page.config-file }} {{ page.config-dir  }}/config-utf16.txt
Get-Content {{ page.config-dir  }}/config-utf16.txt | Set-Content -Encoding UTF8 {{ page.config-dir }}/{{ page.config-file }}
```
## Regenerate Config File with Bash

```bash
# Regenerate Config File
cd ~/github/{{ site.local_repo }}
cp {{ page.config-file }} {{ page.config-dir  }}/{{ page.config-file }}
```

## Generated Config File

```yml
# Include sitemap/config.yml
{% include_relative {{ page.config-file }} %}
```
