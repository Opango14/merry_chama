/**
 * ChamaFlow — Navbar
 * Phase 2: Mobile menu toggle + outside-click close.
 * Loaded by base.html via {% static 'js/navbar.js' %}
 */

(function () {
    'use strict';

    const burger = document.getElementById('nav-toggle');
    const menu   = document.getElementById('nav-menu');
    if (!burger || !menu) return;

    /* ── Toggle ──────────────────────────────────────────────────── */
    function openMenu() {
        menu.classList.add('is-open');
        burger.setAttribute('aria-expanded', 'true');
        burger.setAttribute('aria-label', 'Close menu');
    }

    function closeMenu() {
        menu.classList.remove('is-open');
        burger.setAttribute('aria-expanded', 'false');
        burger.setAttribute('aria-label', 'Open menu');
    }

    function toggleMenu() {
        menu.classList.contains('is-open') ? closeMenu() : openMenu();
    }

    burger.addEventListener('click', toggleMenu);

    /* ── Close on outside click ─────────────────────────────────── */
    document.addEventListener('click', function (e) {
        if (!menu.contains(e.target) && !burger.contains(e.target)) {
            closeMenu();
        }
    });

    /* ── Close on resize past md breakpoint ─────────────────────── */
    window.addEventListener('resize', function () {
        if (window.innerWidth >= 768) closeMenu();
    });

    /* ── Close on Escape key ────────────────────────────────────── */
    document.addEventListener('keydown', function (e) {
        if (e.key === 'Escape') closeMenu();
    });
}());
