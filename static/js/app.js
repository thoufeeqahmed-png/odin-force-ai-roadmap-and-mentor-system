/**
 * ODIN FORCE — Asgardian AI Roadmap Companion
 * Main Application JavaScript
 */

document.addEventListener('DOMContentLoaded', () => {
    // 1. Mobile navigation toggle
    const mobileMenuBtn = document.getElementById('mobile-menu-toggle');
    const mainNav = document.getElementById('main-nav');

    if (mobileMenuBtn && mainNav) {
        mobileMenuBtn.addEventListener('click', () => {
            const isVisible = mainNav.classList.contains('mobile-nav-open');
            if (isVisible) {
                mainNav.classList.remove('mobile-nav-open');
                mainNav.style.display = 'none';
            } else {
                mainNav.classList.add('mobile-nav-open');
                mainNav.style.display = 'flex';
                mainNav.style.flexDirection = 'column';
                mainNav.style.position = 'absolute';
                mainNav.style.top = '100%';
                mainNav.style.left = '0';
                mainNav.style.right = '0';
                mainNav.style.background = '#070b14';
                mainNav.style.padding = '20px';
                mainNav.style.borderBottom = '1px solid rgba(245, 158, 11, 0.2)';
                mainNav.style.boxShadow = '0 16px 40px rgba(0, 0, 0, 0.6)';
                mainNav.style.gap = '12px';
            }
        });
    }

    // 2. Auto-dismiss toast notifications after 5 seconds
    const toasts = document.querySelectorAll('.toast-message');
    toasts.forEach(toast => {
        setTimeout(() => {
            toast.style.opacity = '0';
            toast.style.transform = 'translateX(50px)';
            toast.style.transition = 'all 0.4s ease';
            setTimeout(() => toast.remove(), 400);
        }, 5000);
    });

    // 3. Header background on scroll
    const header = document.getElementById('site-header');
    if (header) {
        window.addEventListener('scroll', () => {
            if (window.scrollY > 40) {
                header.classList.add('scrolled-header');
            } else {
                header.classList.remove('scrolled-header');
            }
        });
    }
});
