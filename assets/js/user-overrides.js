/* ===========================================================================
   IT-Journey — pin the "cosmic quest" dark appearance.
   ---------------------------------------------------------------------------
   Loaded LAST by the zer0-mistakes theme when `user_overrides: true`
   (js-cdn.html). The theme renders data-bs-theme="dark" server-side but the
   color mode otherwise follows the OS (prefers-color-scheme) / the optional
   appearance panel. IT-Journey is an intentionally always-dark branded
   experience (see the landing page), so we keep data-bs-theme + skin pinned to
   "dark" for a consistent look across every page. Pairs with the visual
   overrides in /assets/css/user-overrides.css.
   =========================================================================== */
(function () {
  var root = document.documentElement;
  function pinDark() {
    if (root.getAttribute('data-bs-theme') !== 'dark') root.setAttribute('data-bs-theme', 'dark');
    if (root.getAttribute('data-theme-skin') !== 'dark') root.setAttribute('data-theme-skin', 'dark');
  }
  pinDark();
  // Re-assert if the OS theme changes or the appearance panel writes a new value.
  try {
    var mq = window.matchMedia('(prefers-color-scheme: light)');
    if (mq.addEventListener) mq.addEventListener('change', pinDark);
  } catch (e) { /* no-op */ }
  document.addEventListener('DOMContentLoaded', pinDark);
})();
