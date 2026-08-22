/*
 * notes-markdown.js — a small markdown renderer for notes written in the browser.
 *
 * Public notes are rendered by Jekyll with kramdown, so this is only for the
 * local notes a reader writes in the workbench editor. It covers the subset
 * that shows up in real notes — headings, fenced code, lists, tables, links,
 * emphasis, blockquotes, and [[wiki links]] — with no dependency to download.
 *
 * SECURITY CONTRACT, and the reason this file exists rather than a library:
 * the source is HTML-escaped ONCE, up front, before any transform runs. Every
 * rule below therefore operates on text that can no longer contain a tag, and
 * the only markup in the output is markup this file wrote itself. There is no
 * sanitizer to keep ahead of and no raw-HTML passthrough to get wrong — a note
 * containing <script> renders as the visible characters "<script>".
 *
 * The one place a URL reaches an attribute is linkHref(), which allows only
 * http(s) and site-relative targets; anything else (javascript:, data:, vbscript:)
 * is dropped. Callers may assign the result to innerHTML; that is the whole
 * point of the escape-first design.
 */
(function () {
  'use strict';

  function escapeHtml(s) {
    return String(s)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#39;');
  }

  // Only http(s) and same-site paths survive. Everything else returns null and
  // the link is rendered as plain text instead.
  function linkHref(raw) {
    var url = String(raw || '').trim();
    if (!url) return null;
    // The source was escaped already, so an author's & arrives as &amp;.
    var probe = url.replace(/&amp;/g, '&').toLowerCase();
    if (/^(https?:)?\/\//.test(probe)) return url;
    if (probe.charAt(0) === '/' || probe.charAt(0) === '#') return url;
    if (/^[a-z][a-z0-9+.-]*:/.test(probe)) return null; // javascript:, data:, mailto:…
    return url; // a bare relative path
  }

  // Resolvers are supplied by the workbench: given a [[Title]], return
  // { url, title } for a page that exists, or null to offer creating a note.
  var resolver = null;
  function setResolver(fn) { resolver = typeof fn === 'function' ? fn : null; }

  function inline(text) {
    var out = text;

    // Code spans first: their contents must not pick up any later rule.
    var spans = [];
    out = out.replace(/`([^`\n]+)`/g, function (m, code) {
      spans.push('<code>' + code + '</code>');
      return '\u0000CODE' + (spans.length - 1) + '\u0000';
    });

    // [[Wiki Link]] and [[Target|label]]
    out = out.replace(/\[\[([^\]|]+)(?:\|([^\]]+))?\]\]/g, function (m, target, label) {
      var name = target.trim();
      var text = (label || name).trim();
      var hit = resolver ? resolver(name) : null;
      if (hit && hit.url) {
        var href = linkHref(hit.url);
        if (href) return '<a class="nw-wikilink" href="' + href + '">' + text + '</a>';
      }
      return '<button type="button" class="nw-wikilink nw-wikilink--new" data-nw-create="' + name + '">' + text + '</button>';
    });

    // ![alt](src) — images are rendered as a link, not an <img>: a note should
    // not be able to fire off a request to an arbitrary host just by being shown.
    out = out.replace(/!\[([^\]]*)\]\(([^)\s]+)(?:\s+"[^"]*")?\)/g, function (m, alt, src) {
      var href = linkHref(src);
      var label = alt || 'image';
      if (!href) return label;
      return '<a class="nw-md-img" href="' + href + '" rel="noopener noreferrer" target="_blank">🖼 ' + label + '</a>';
    });

    // [text](url)
    out = out.replace(/\[([^\]]+)\]\(([^)\s]+)(?:\s+"[^"]*")?\)/g, function (m, label, url) {
      var href = linkHref(url);
      if (!href) return label;
      var ext = /^(https?:)?\/\//.test(href.replace(/&amp;/g, '&'));
      return '<a href="' + href + '"' + (ext ? ' rel="noopener noreferrer" target="_blank"' : '') + '>' + label + '</a>';
    });

    out = out.replace(/\*\*([^*\n]+)\*\*/g, '<strong>$1</strong>');
    out = out.replace(/__([^_\n]+)__/g, '<strong>$1</strong>');
    out = out.replace(/(^|[^*])\*([^*\n]+)\*/g, '$1<em>$2</em>');
    out = out.replace(/~~([^~\n]+)~~/g, '<del>$1</del>');

    out = out.replace(/\u0000CODE(\d+)\u0000/g, function (m, i) {
      var span = spans[Number(i)];
      return span === undefined ? m : span;
    });
    return out;
  }

  function tableRow(line) {
    var cells = line.replace(/^\s*\|/, '').replace(/\|\s*$/, '').split('|');
    return cells.map(function (c) { return c.trim(); });
  }

  function isDivider(line) {
    return /^\s*\|?\s*:?-{2,}:?\s*(\|\s*:?-{2,}:?\s*)*\|?\s*$/.test(line);
  }

  function render(src) {
    if (!src) return '';
    var lines = escapeHtml(String(src).replace(/\r\n?/g, '\n')).split('\n');
    var html = [];
    var i = 0;
    var listStack = [];

    function closeLists(toDepth) {
      while (listStack.length > toDepth) html.push(listStack.pop() === 'ol' ? '</ol>' : '</ul>');
    }

    while (i < lines.length) {
      var line = lines[i];

      // fenced code
      var fence = line.match(/^\s*(```+|~~~+)\s*([A-Za-z0-9_+-]*)\s*$/);
      if (fence) {
        closeLists(0);
        var marker = fence[1].charAt(0) === '`' ? '```' : '~~~';
        var lang = fence[2] || '';
        var buf = [];
        i += 1;
        while (i < lines.length && !new RegExp('^\\s*' + marker).test(lines[i])) {
          buf.push(lines[i]);
          i += 1;
        }
        i += 1; // closing fence
        html.push('<pre><code' + (lang ? ' class="language-' + lang + '"' : '') + '>' + buf.join('\n') + '</code></pre>');
        continue;
      }

      // table: a header row followed by a divider row
      if (/\|/.test(line) && i + 1 < lines.length && isDivider(lines[i + 1])) {
        closeLists(0);
        var head = tableRow(line);
        html.push('<table class="nw-md-table"><thead><tr>');
        head.forEach(function (c) { html.push('<th>' + inline(c) + '</th>'); });
        html.push('</tr></thead><tbody>');
        i += 2;
        while (i < lines.length && /\|/.test(lines[i]) && lines[i].trim()) {
          html.push('<tr>');
          tableRow(lines[i]).forEach(function (c) { html.push('<td>' + inline(c) + '</td>'); });
          html.push('</tr>');
          i += 1;
        }
        html.push('</tbody></table>');
        continue;
      }

      // heading
      var h = line.match(/^(#{1,6})\s+(.*)$/);
      if (h) {
        closeLists(0);
        var level = h[1].length;
        html.push('<h' + level + '>' + inline(h[2].trim()) + '</h' + level + '>');
        i += 1;
        continue;
      }

      // horizontal rule
      if (/^\s*([-*_])(\s*\1){2,}\s*$/.test(line)) {
        closeLists(0);
        html.push('<hr>');
        i += 1;
        continue;
      }

      // blockquote
      if (/^\s*&gt;\s?/.test(line)) {
        closeLists(0);
        var quote = [];
        while (i < lines.length && /^\s*&gt;\s?/.test(lines[i])) {
          quote.push(lines[i].replace(/^\s*&gt;\s?/, ''));
          i += 1;
        }
        html.push('<blockquote>' + inline(quote.join(' ')) + '</blockquote>');
        continue;
      }

      // task list, bullet list, ordered list
      var li = line.match(/^(\s*)([-*+]|\d+[.)])\s+(.*)$/);
      if (li) {
        var depth = Math.floor(li[1].length / 2) + 1;
        var ordered = /\d/.test(li[2]);
        while (listStack.length < depth) {
          html.push(ordered ? '<ol>' : '<ul>');
          listStack.push(ordered ? 'ol' : 'ul');
        }
        closeLists(depth);
        var body = li[3];
        var task = body.match(/^\[([ xX])\]\s+(.*)$/);
        if (task) {
          html.push('<li class="nw-md-task"><input type="checkbox" disabled' +
            (task[1] === ' ' ? '' : ' checked') + '> ' + inline(task[2]) + '</li>');
        } else {
          html.push('<li>' + inline(body) + '</li>');
        }
        i += 1;
        continue;
      }

      // blank line
      if (!line.trim()) {
        closeLists(0);
        i += 1;
        continue;
      }

      // Paragraph: gather until a blank line or a block-level construct. The
      // first line is always consumed, even if it looks like the start of a
      // block that no branch above claimed (an unterminated ``` with trailing
      // text, say) — otherwise this loop could make no progress at all.
      closeLists(0);
      var para = [lines[i]];
      i += 1;
      while (i < lines.length && lines[i].trim() &&
             !/^(#{1,6})\s/.test(lines[i]) &&
             !/^\s*(```+|~~~+)/.test(lines[i]) &&
             !/^\s*&gt;\s?/.test(lines[i]) &&
             !/^(\s*)([-*+]|\d+[.)])\s+/.test(lines[i]) &&
             !/^\s*([-*_])(\s*\1){2,}\s*$/.test(lines[i])) {
        para.push(lines[i]);
        i += 1;
      }
      if (para.length) html.push('<p>' + inline(para.join(' ')) + '</p>');
    }

    closeLists(0);
    return html.join('\n');
  }

  // A short plain-text preview for card summaries and search — no markup at all.
  function excerpt(src, max) {
    var limit = max || 180;
    var text = String(src || '')
      .replace(/```[\s\S]*?```/g, ' ')
      .replace(/`([^`]+)`/g, '$1')
      .replace(/!?\[([^\]]*)\]\([^)]*\)/g, '$1')
      .replace(/\[\[([^\]|]+)(?:\|([^\]]+))?\]\]/g, function (m, t, l) { return l || t; })
      .replace(/^#{1,6}\s+/gm, '')
      .replace(/[*_~>]/g, '')
      .replace(/\s+/g, ' ')
      .trim();
    return text.length > limit ? text.slice(0, limit - 1) + '…' : text;
  }

  window.ITJMarkdown = {
    render: render,
    excerpt: excerpt,
    escapeHtml: escapeHtml,
    setWikiResolver: setResolver
  };
}());
