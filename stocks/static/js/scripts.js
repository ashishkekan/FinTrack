document.addEventListener('DOMContentLoaded', function () {
    // Mobile Navbar Toggle
    const navbarToggle = document.getElementById('navbarToggle');
    const mobileMenu = document.getElementById('mobileMenu');

    if (navbarToggle && mobileMenu) {
        navbarToggle.addEventListener('click', () => {
            mobileMenu.classList.toggle('active');
        });
    }
});