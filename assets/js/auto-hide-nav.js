// Hides the navbar when scrolling down half a page and shows it when scrolling up
window.onload = function() {
    let lastScrollTop = 0;
    const navbar = document.getElementById('navbar');

    window.addEventListener('scroll', function() {
        let scrollTop = window.pageYOffset || document.documentElement.scrollTop;
        let halfPageHeight = window.innerHeight / 2;

        if (scrollTop > lastScrollTop && scrollTop > halfPageHeight) {
            navbar.classList.add('hide-navbar');
            navbar.classList.add('fixed-navbar');
        } else {
            navbar.classList.remove('hide-navbar');
        }
        lastScrollTop = scrollTop;
    });
}