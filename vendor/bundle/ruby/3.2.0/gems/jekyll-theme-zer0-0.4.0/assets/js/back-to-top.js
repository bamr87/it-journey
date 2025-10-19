document.addEventListener('DOMContentLoaded', () => {
  const btn = document.getElementById('backToTopBtn');
  if (!btn) return;

  // Smooth scroll to top and keep accessible
  const scrollToTop = (e) => {
    if (e) e.preventDefault();
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  btn.addEventListener('click', scrollToTop);

  const toggle = () => {
    const y = window.scrollY || document.documentElement.scrollTop || document.body.scrollTop || 0;
    btn.style.display = y > 200 ? 'block' : 'none';
  };

  // Initialize state and bind listener without clobbering
  toggle();
  window.addEventListener('scroll', toggle, { passive: true });
});
