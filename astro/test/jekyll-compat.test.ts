import assert from 'node:assert/strict';
import { test } from 'node:test';

import { buildIndex, splitFrontmatter, translate } from '../src/lib/jekyll-compat.ts';

const index = buildIndex([
  { file: 'pages/_quests/0001/README.md', permalink: '/quests/0001/', title: 'Level 0001 - Web Fundamentals' },
  { file: 'pages/_quests/0001/forge-your-character.md', permalink: '/quests/0001/forge-your-character/', title: 'Forge Your Character' },
  { file: 'pages/_quests/0001/github-pages-portal.md', permalink: '/quests/0001/github-pages-portal/', title: 'The GitHub Pages Portal' },
]);

const run = (body: string, extra: Partial<Parameters<typeof translate>[1]> = {}) =>
  translate(body, { file: 'pages/_quests/0001/avatar-forge.md', index, ...extra });

test('splitFrontmatter separates YAML from the body', () => {
  const { frontmatter, body } = splitFrontmatter('---\ntitle: A\n---\n# Hi\n');
  assert.equal(frontmatter, 'title: A');
  assert.equal(body, '# Hi\n');
  assert.equal(splitFrontmatter('no front matter').frontmatter, null);
});

test('raw blocks are unwrapped and their Liquid stays literal', () => {
  const src = '{% raw %}\n```yaml\nrun: ${{ secrets.TOKEN }}\n```\n{% endraw %}\n\nUse {% raw %}`{% include x.html %}`{% endraw %} here.';
  const { body, issues, stats } = run(src);
  assert.ok(body.includes('run: ${{ secrets.TOKEN }}'));
  assert.ok(body.includes('`{% include x.html %}`'));
  assert.ok(!body.includes('raw %}'));
  assert.equal(stats.rawBlocks, 2);
  assert.deepEqual(issues, []);
});

test('Liquid outside raw is removed and reported', () => {
  const { body, issues } = run('Before\n\n{% include quest-card.html quest=q %}\n\n{% for q in site.quests %}row{% endfor %}\n\nTotal: {{ site.data.stats.total }}');
  assert.ok(!body.includes('{%'));
  assert.ok(!body.includes('{{'));
  assert.deepEqual(
    issues.map((i) => i.kind),
    ['liquid-output', 'liquid-tag', 'liquid-tag', 'liquid-tag'],
  );
  assert.equal(issues[1]?.detail, 'include quest-card.html quest=q');
});

test('known Liquid outputs are substituted, not reported', () => {
  const { body, issues, stats } = run("[home]({{ site.baseurl }}/quests/) and [x]({{ '/quests/0001/' | relative_url }})", {
    vars: { 'site.baseurl': '' },
  });
  assert.equal(body, '[home](/quests/) and [x](/quests/0001/)');
  assert.equal(stats.liquidOutputsSubstituted, 2);
  assert.deepEqual(issues, []);
});

test('unwrapped Liquid inside a code fence is kept and flagged', () => {
  const { body, issues } = run('```liquid\n{{ page.title }}\n```');
  assert.ok(body.includes('{{ page.title }}'));
  assert.equal(issues[0]?.kind, 'liquid-in-code');
});

test('comments vanish and highlight becomes a fence', () => {
  const { body, stats } = run('A{% comment %}hidden{% endcomment %}B\n\n{% highlight ruby %}\nputs 1\n{% endhighlight %}');
  assert.ok(body.startsWith('AB'));
  assert.ok(body.includes('```ruby\nputs 1\n```'));
  assert.equal(stats.liquidComments, 1);
  assert.equal(stats.highlightBlocks, 1);
});

test('<details markdown="1"> gets the blank lines CommonMark needs', () => {
  const src = '<details markdown="1">\n<summary>Solution</summary>\n```bash\nls\n```\n</details>';
  const { body, stats } = run(src);
  assert.equal(body, '<details>\n<summary>Solution</summary>\n\n```bash\nls\n```\n\n</details>');
  assert.equal(stats.detailsFixed, 1);
});

test('attribute lists are stripped, including the TOC marker', () => {
  const { body, stats } = run('# T\n\n* TOC\n{:toc}\n\nA [link](https://x.dev){:target="_blank"} here.\n\n{: .lead}');
  assert.ok(!body.includes('{:'));
  assert.ok(!/TOC/.test(body));
  assert.ok(body.includes('A [link](https://x.dev) here.'));
  assert.equal(stats.attributeListsStripped, 3);
});

test('wikilinks resolve by title or basename; bash tests and code are left alone', () => {
  const src = 'See [[Level 0001 - Web Fundamentals]] and [[forge-your-character|your hero]].\n\nNot `[[this]]` and not [[ -f file ]].\n\n```bash\n[[ -d dir ]] && echo ok\n```\n\n[[Nowhere]]';
  const { body, issues, stats } = run(src);
  assert.ok(body.includes('[Level 0001 - Web Fundamentals](/quests/0001/)'));
  assert.ok(body.includes('[your hero](/quests/0001/forge-your-character/)'));
  assert.ok(body.includes('`[[this]]`'));
  assert.ok(body.includes('[[ -f file ]]'));
  assert.ok(body.includes('[[ -d dir ]] && echo ok'));
  assert.equal(stats.wikilinksResolved, 2);
  assert.deepEqual(issues, [{ kind: 'wikilink-unresolved', detail: '[[Nowhere]]' }]);
});

test('a backslash in a wikilink label stays literal and cannot break the link', () => {
  const { body, stats } = run('Open [[forge-your-character|C:\\]] first.');
  assert.ok(body.includes('[C:\\\\](/quests/0001/forge-your-character/)'));
  assert.equal(stats.wikilinksResolved, 1);
});

test('relative .md links become permalinks and keep their fragment', () => {
  const { body, issues, stats } = run('[portal](github-pages-portal.md#deploy), [level](./README.md), [gone](missing.md), [ext](https://x.dev/a.md)');
  assert.ok(body.includes('[portal](/quests/0001/github-pages-portal/#deploy)'));
  assert.ok(body.includes('[level](/quests/0001/)'));
  assert.ok(body.includes('[gone](missing.md)'));
  assert.ok(body.includes('[ext](https://x.dev/a.md)'));
  assert.equal(stats.relativeLinksResolved, 2);
  assert.deepEqual(issues, [{ kind: 'relative-link-unresolved', detail: 'missing.md' }]);
});

test('a leading H1 is dropped only when asked, and only when it comes first', () => {
  const src = '# Title\n\nIntro\n\n## Two';
  assert.equal(run(src, { stripLeadingH1: true }).body, 'Intro\n\n## Two');
  assert.equal(run(src).body, src);
  const later = '## First\n\n# Later';
  assert.equal(run(later, { stripLeadingH1: true }).body, later);
  const inFence = '```md\n# not a heading\n```\n\n# Real';
  assert.equal(run(inFence, { stripLeadingH1: true }).body, '```md\n# not a heading\n```\n');
});

test('mermaid fences are counted', () => {
  assert.equal(run('```mermaid\ngraph TD; A-->B\n```').stats.mermaidFences, 1);
});
