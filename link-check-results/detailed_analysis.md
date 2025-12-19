# IT-Journey Link Health Analysis Report

**Analysis Date**: 2025-12-12T03:38:37.541716Z
**Total Links**: 78344
**Broken Links**: 10680
**Success Rate**: 82.1%

## Failure Categories

### Broken External
**Count**: 10266

- **URL**: https://it-journey.dev/terms-of-service
  - **File**: _site/quests/level-0101-workflow-optimization/index.html
  - **Error**: {'text': 'error (cached)', 'code': 404}

- **URL**: https://it-journey.dev/tags/#gamified-learning
  - **File**: _site/quests/level-0101-workflow-optimization/index.html
  - **Error**: {'text': 'error (cached)', 'code': 404}

- **URL**: https://it-journey.dev/about/theme
  - **File**: _site/quests/level-0101-workflow-optimization/index.html
  - **Error**: {'text': 'error (cached)', 'code': 404}

- **URL**: https://it-journey.dev/subscribe
  - **File**: _site/quests/level-0101-workflow-optimization/index.html
  - **Error**: {'text': 'error (cached)', 'code': 404}

- **URL**: https://it-journey.dev/contact
  - **File**: _site/quests/level-0101-workflow-optimization/index.html
  - **Error**: {'text': 'error (cached)', 'code': 404}

... and 10261 more

### Timeouts
**Count**: 12

- **URL**: http://memory.loc.gov/ammem/collections/sheetmusic/brown/
  - **File**: pages/_posts/creative & experimental/2025-07-03-music-resources-free-sheet-music.md
  - **Error**: {'text': 'timeout'}

- **URL**: http://memory.loc.gov/ammem/smhtml/smhome.html
  - **File**: pages/_posts/creative & experimental/2025-07-03-music-resources-free-sheet-music.md
  - **Error**: {'text': 'timeout'}

- **URL**: http://memory.loc.gov/ammem/collections/sheetmusic/brown/
  - **File**: link-check-results/summary.md
  - **Error**: {'text': 'timeout'}

- **URL**: http://254.169.254.169/latest/meta-data
  - **File**: link-check-results/summary.md
  - **Error**: {'text': 'timeout'}

- **URL**: http://memory.loc.gov/ammem/smhtml/smhome.html
  - **File**: link-check-results/summary.md
  - **Error**: {'text': 'timeout'}

... and 7 more

### Rate Limited
**Count**: 44

- **URL**: https://reddit.com/r/Jekyll
  - **File**: _site/quests/stating-the-stats/index.html
  - **Error**: {'text': 'rejected status code (this depends on your "accept" configuration)', 'code': 429}

- **URL**: https://reddit.com/r/devops
  - **File**: pages/_posts/2025-11-16-work-directory-ci-cd.md
  - **Error**: {'text': 'rejected status code (this depends on your "accept" configuration)', 'code': 429}

- **URL**: https://reddit.com/r/Jekyll
  - **File**: pages/_quests/0001/stating-the-stats.md
  - **Error**: {'text': 'rejected status code (this depends on your "accept" configuration)', 'code': 429}

- **URL**: https://reddit.com/r/bash
  - **File**: pages/_quests/0010/bash-scripting.md
  - **Error**: {'text': 'rejected status code (this depends on your "accept" configuration)', 'code': 429}

- **URL**: https://stackshare.io/
  - **File**: _site/quests/level-0001/stack-attack/index.html
  - **Error**: {'text': 'error (cached)', 'code': 429}

... and 39 more

### Certificate Errors
**Count**: 370

- **URL**: http://0.0.0.0:4002/quests/level-0111-error-handling/
  - **File**: _site/quests/level-0111-error-handling/index.html
  - **Error**: {'text': 'network error', 'details': 'error sending request for url (http://0.0.0.0:4002/quests/level-0111-error-handling/) maybe a certificate error?'}

- **URL**: http://0.0.0.0:4002/posts/2024/04/25/placeholders/
  - **File**: _site/posts/2024/04/25/placeholders/index.html
  - **Error**: {'text': 'network error', 'details': 'error sending request for url (http://0.0.0.0:4002/posts/2024/04/25/placeholders/) maybe a certificate error?'}

- **URL**: http://0.0.0.0:4002/posts/2025/11/16/jekyll-and-travis/
  - **File**: _site/posts/2025/11/16/jekyll-and-travis/index.html
  - **Error**: {'text': 'network error', 'details': 'error sending request for url (http://0.0.0.0:4002/posts/2025/11/16/jekyll-and-travis/) maybe a certificate error?'}

- **URL**: http://0.0.0.0:4002/quests/vscode-mastery/
  - **File**: _site/quests/vscode-mastery/index.html
  - **Error**: {'text': 'network error', 'details': 'error sending request for url (http://0.0.0.0:4002/quests/vscode-mastery/) maybe a certificate error?'}

- **URL**: http://0.0.0.0:4002/pages/11/
  - **File**: _site/pages/12/index.html
  - **Error**: {'text': 'network error', 'details': 'error sending request for url (http://0.0.0.0:4002/pages/11/) maybe a certificate error?'}

... and 365 more

## Identified Patterns

- Top failing domains: it-journey.dev(9031), 0.0.0.0:4002(726), github.com(365)
- High timeout rate (12) - network or slow sites

## Recommendations

### Priority Actions

1. **Fix Internal Links**: Address broken internal navigation first
2. **Update External Links**: Replace or remove broken external references
3. **Monitor SSL/DNS Issues**: Review certificate and domain problems
4. **Consider Rate Limiting**: Add problematic domains to ignore list
