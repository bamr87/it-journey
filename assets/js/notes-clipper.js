/*
 * notes-clipper.js — capture a snippet from any page into the notes workbench.
 *
 * This is what makes /notes/ a workbench rather than a folder: while you are
 * reading a quest you can grab the command you just ran, or the paragraph that
 * explained why, and it lands on your board with a link back to the exact
 * heading you took it from.
 *
 * Loaded site-wide from _includes/custom/body-end.html — every page except the
 * workbench itself, which has its own richer UI.
 *
 * Three ways to clip:
 *   1. a button beside the copy button on every code block
 *   2. a popover when you select text in the page body
 *   3. a "pin this page" control, so a whole page can be referenced
 *
 * All three are injected, so a theme change can only cost a feature, never a
 * page: every hook is looked up defensively and skipped when it is not there.
 */
(function () {
  'use strict';

  var store = window.ITJNotes;
  if (!store) return;
  // The workbench renders its own affordances; nothing to inject there.
  if (document.getElementById('notes-workbench')) return;

  var main = document.getElementById('main-content') || document.querySelector('main') || document.body;
  if (!main) return;

  var meta = {
    url: metaContent('itj:url') || window.location.pathname,
    title: metaContent('itj:title') || document.title || window.location.pathname,
    collection: metaContent('itj:collection') || ''
  };
  var workbenchUrl = metaContent('itj:workbench') || '/notes/';

  function metaContent(name) {
    var el = document.querySelector('meta[name="' + name + '"]');
    return el ? el.getAttribute('content') : null;
  }

  // ---- toast ---------------------------------------------------------------

  var toastEl = null;
  var toastTimer = null;

  function toast(message) {
    if (!toastEl) {
      toastEl = document.createElement('div');
      toastEl.className = 'itj-clip-toast';
      toastEl.setAttribute('role', 'status');
      toastEl.setAttribute('aria-live', 'polite');
      document.body.appendChild(toastEl);
    }
    toastEl.textContent = '';
    var text = document.createElement('span');
    text.textContent = message;
    var link = document.createElement('a');
    link.className = 'itj-clip-toast__link';
    link.href = workbenchUrl;
    link.textContent = 'Open workbench';
    toastEl.appendChild(text);
    toastEl.appendChild(link);
    toastEl.classList.add('is-visible');
    if (toastTimer) clearTimeout(toastTimer);
    toastTimer = setTimeout(function () { toastEl.classList.remove('is-visible'); }, 4200);
  }

  // ---- where did this come from -------------------------------------------
  // Walk backwards through the document for the nearest heading that has an id,
  // so the clip can link to the exact section rather than the page top.

  function nearestHeading(node) {
    var el = node && node.nodeType === 1 ? node : (node ? node.parentElement : null);
    while (el && el !== main) {
      var prev = el.previousElementSibling;
      while (prev) {
        if (/^H[1-6]$/.test(prev.tagName)) {
          return { text: (prev.textContent || '').trim(), id: prev.id || '' };
        }
        var nested = prev.querySelectorAll ? prev.querySelectorAll('h1,h2,h3,h4,h5,h6') : [];
        if (nested.length) {
          var last = nested[nested.length - 1];
          return { text: (last.textContent || '').trim(), id: last.id || '' };
        }
        prev = prev.previousElementSibling;
      }
      el = el.parentElement;
    }
    return { text: '', id: '' };
  }

  function sourceUrlFor(heading) {
    return meta.url + (heading && heading.id ? '#' + heading.id : '');
  }

  function saveClip(fields) {
    var heading = fields.heading || { text: '', id: '' };
    store.addClip({
      kind: fields.kind,
      text: fields.text,
      lang: fields.lang || '',
      heading: heading.text || '',
      sourceUrl: sourceUrlFor(heading),
      sourceTitle: meta.title,
      sourceCollection: meta.collection
    });
    toast(fields.kind === 'code' ? 'Code clipped.' : 'Selection clipped.');
  }

  // ---- code blocks ---------------------------------------------------------
  // The theme's code-copy.js wraps each <pre> and builds a .code-block-header
  // holding a language label and a copy button. It is deferred like this file,
  // so rather than racing it we watch for the headers to appear.

  function languageOf(scope) {
    var code = scope.querySelector('code');
    var cls = (code && code.className) || '';
    var m = cls.match(/language-([A-Za-z0-9_+-]+)/);
    if (m) return m[1];
    var label = scope.querySelector('.code-block-label, .code-block-header__label');
    return label ? (label.textContent || '').trim().toLowerCase() : '';
  }

  function codeTextOf(scope) {
    var code = scope.querySelector('code') || scope.querySelector('pre');
    return code ? (code.innerText || code.textContent || '') : '';
  }

  function clipButton(label) {
    var b = document.createElement('button');
    b.type = 'button';
    b.className = 'itj-clip-btn';
    b.setAttribute('data-itj-clip', '');
    b.setAttribute('aria-label', label);
    b.title = label;
    // Labelled like the copy button it sits beside — a bare pair of scissors
    // does not tell anyone where the snippet is about to go.
    b.innerHTML = '<i class="bi bi-scissors" aria-hidden="true"></i>' +
      '<span class="itj-clip-btn__text">Clip</span>';
    return b;
  }

  function decorateHeaders() {
    var headers = main.querySelectorAll('.code-block-header');
    Array.prototype.forEach.call(headers, function (header) {
      if (header.querySelector('[data-itj-clip]')) return;
      var wrapper = header.parentElement;
      if (!wrapper) return;
      var btn = clipButton('Clip this code to your notes');
      btn.addEventListener('click', function () {
        var text = codeTextOf(wrapper);
        if (!text.trim()) return;
        saveClip({ kind: 'code', text: text, lang: languageOf(wrapper), heading: nearestHeading(wrapper) });
      });
      header.appendChild(btn);
      // Claim this block's <pre> so the late fallback below knows it is served.
      // Marking the element beats inferring it from how deeply the theme nests
      // its wrappers, which is exactly the thing a theme update changes.
      var claimed = wrapper.querySelectorAll('pre');
      Array.prototype.forEach.call(claimed, function (pre) {
        pre.setAttribute('data-itj-clip-done', '1');
      });
    });
  }

  // The theme builds its headers in the browser, not at build time, so a <pre>
  // with no header yet usually just means code-copy.js has not run. This is the
  // late fallback: once things have settled, anything still bare gets a button
  // of its own, so a theme change costs styling rather than the feature.
  function decorateBarePres() {
    var pres = main.querySelectorAll('pre');
    Array.prototype.forEach.call(pres, function (pre) {
      // Set either by decorateHeaders(), meaning this block already has a
      // button, or by a previous pass of this function.
      if (pre.getAttribute('data-itj-clip-done')) return;
      pre.setAttribute('data-itj-clip-done', '1');
      var holder = document.createElement('div');
      holder.className = 'itj-clip-bare';
      var btn = clipButton('Clip this code to your notes');
      btn.addEventListener('click', function () {
        var text = pre.innerText || pre.textContent || '';
        if (!text.trim()) return;
        saveClip({ kind: 'code', text: text, lang: languageOf(pre), heading: nearestHeading(pre) });
      });
      holder.appendChild(btn);
      if (pre.parentElement) pre.parentElement.insertBefore(holder, pre);
    });
  }

  decorateHeaders();

  if (window.MutationObserver) {
    var scanTimer = null;
    var observer = new MutationObserver(function () {
      // Our own insertions re-trigger this, so coalesce before looking again.
      if (scanTimer) clearTimeout(scanTimer);
      scanTimer = setTimeout(decorateHeaders, 60);
    });
    observer.observe(main, { childList: true, subtree: true });
    setTimeout(function () {
      observer.disconnect();
      if (scanTimer) clearTimeout(scanTimer);
      decorateHeaders();
      decorateBarePres();
    }, 2500);
  } else {
    setTimeout(function () {
      decorateHeaders();
      decorateBarePres();
    }, 2500);
  }

  // ---- text selection ------------------------------------------------------

  var popover = null;

  function hidePopover() {
    if (popover) popover.classList.remove('is-visible');
  }

  function showPopover(rect, onClip) {
    if (!popover) {
      popover = document.createElement('div');
      popover.className = 'itj-clip-pop';
      popover.innerHTML = '<button type="button" class="itj-clip-pop__btn">' +
        '<i class="bi bi-scissors" aria-hidden="true"></i> Clip selection</button>';
      document.body.appendChild(popover);
    }
    var btn = popover.querySelector('.itj-clip-pop__btn');
    btn.onclick = function () {
      onClip();
      hidePopover();
      var sel = window.getSelection();
      if (sel && sel.removeAllRanges) sel.removeAllRanges();
    };
    var top = rect.top + window.pageYOffset - 44;
    var left = rect.left + window.pageXOffset + (rect.width / 2);
    popover.style.top = Math.max(window.pageYOffset + 8, top) + 'px';
    popover.style.left = left + 'px';
    popover.classList.add('is-visible');
  }

  document.addEventListener('mouseup', function (ev) {
    if (popover && popover.contains(ev.target)) return;
    setTimeout(function () {
      var sel = window.getSelection();
      if (!sel || sel.isCollapsed) { hidePopover(); return; }
      var text = String(sel).trim();
      if (text.length < 12) { hidePopover(); return; }
      var anchor = sel.anchorNode;
      if (!anchor || !main.contains(anchor.nodeType === 1 ? anchor : anchor.parentElement)) {
        hidePopover();
        return;
      }
      var range = sel.getRangeAt(0);
      var rect = range.getBoundingClientRect();
      if (!rect || (!rect.width && !rect.height)) { hidePopover(); return; }
      showPopover(rect, function () {
        saveClip({ kind: 'text', text: text, heading: nearestHeading(anchor) });
      });
    }, 10);
  });

  document.addEventListener('scroll', hidePopover, { passive: true });
  document.addEventListener('keydown', function (ev) {
    if (ev.key === 'Escape') hidePopover();
  });

  // ---- pin this page -------------------------------------------------------
  // Notes get a small toolbar of their own; every other page can still be
  // pinned from the workbench's search, so this stays out of the way.

  if (meta.collection === 'notes') {
    var host = main.querySelector('h1');
    if (host && host.parentElement) {
      var bar = document.createElement('div');
      bar.className = 'itj-clip-pagebar';

      var pin = document.createElement('button');
      pin.type = 'button';
      pin.className = 'itj-clip-pagebar__btn';
      pin.innerHTML = '<i class="bi bi-pin-angle" aria-hidden="true"></i> Pin to workbench';
      pin.addEventListener('click', function () {
        store.addPin({
          url: meta.url,
          title: meta.title,
          collection: meta.collection,
          description: metaContent('description') || ''
        });
        toast('Pinned this note.');
      });

      var open = document.createElement('a');
      open.className = 'itj-clip-pagebar__link';
      open.href = workbenchUrl;
      open.innerHTML = '<i class="bi bi-clipboard2-check" aria-hidden="true"></i> Workbench';

      bar.appendChild(pin);
      bar.appendChild(open);
      host.parentElement.insertBefore(bar, host.nextSibling);
    }
  }
}());
