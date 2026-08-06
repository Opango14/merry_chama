/**
 * ChamaFlow — Dashboard
 * Phase 4: Card entrance animations.
 * Loaded by dashboard.html via {% static 'js/dashboard.js' %}
 *
 * Depends on GSAP (loaded globally in base.html).
 */

(function () {
    'use strict';

    /* ── Card stagger entrance ─────────────────────────────────────
       Waits 0.85s so the SplitText heading finishes first,
       then staggers the cards up from y:24 to y:0.
    ──────────────────────────────────────────────────────────────── */
    function animateCards() {
        const cards = document.querySelectorAll('.dash-card');
        if (!cards.length || typeof gsap === 'undefined') return;

        gsap.fromTo(
            cards,
            { y: 28, opacity: 0, scale: 0.98 },
            {
                y: 0,
                opacity: 1,
                scale: 1,
                duration: 0.6,
                ease: 'power3.out',
                stagger: { each: 0.09, from: 'start' },
                delay: 0.85
            }
        );
    }

    /* ── Action buttons entrance ───────────────────────────────────
       Slides in from the right slightly after the heading.
    ──────────────────────────────────────────────────────────────── */
    function animateActionBtns() {
        const btns = document.querySelectorAll('.dash-actions__btns .btn');
        if (!btns.length || typeof gsap === 'undefined') return;

        gsap.fromTo(
            btns,
            { x: 16, opacity: 0 },
            {
                x: 0,
                opacity: 1,
                duration: 0.5,
                ease: 'power3.out',
                stagger: { each: 0.08, from: 'end' },
                delay: 0.55
            }
        );
    }

    /* ── Run after DOM is ready ─────────────────────────────────── */
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', function () {
            animateCards();
            animateActionBtns();
        });
    } else {
        animateCards();
        animateActionBtns();
    }
}());
