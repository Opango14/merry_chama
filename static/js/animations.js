/**
 * MerryChama — Animations
 * Phase 9: Scroll-reveal (IntersectionObserver) + GSAP number counter.
 * Loaded globally via base.html via {% static 'js/animations.js' %}
 *
 * Features:
 *  1. Scroll-reveal   — adds .is-visible to .anim-reveal elements when they
 *                       enter the viewport (CSS handles the transition).
 *  2. Number counter  — animates any [data-count-up] element from 0 to its
 *                       numeric value using GSAP, triggered on scroll entry.
 *                       Adds .count-up-done for the pop keyframe.
 */

(function () {
    'use strict';

    /* ── 1. Scroll-reveal (CSS-driven, no GSAP needed) ─────────────
       Add class="anim-reveal" to any element you want to fade-up
       when it enters the viewport.
    ──────────────────────────────────────────────────────────────── */
    function initScrollReveal() {
        const targets = document.querySelectorAll('.anim-reveal');
        if (!targets.length) return;

        const observer = new IntersectionObserver(
            function (entries) {
                entries.forEach(function (entry) {
                    if (entry.isIntersecting) {
                        entry.target.classList.add('is-visible');
                        observer.unobserve(entry.target); // once only
                    }
                });
            },
            { threshold: 0.12, rootMargin: '0px 0px -24px 0px' }
        );

        targets.forEach(function (el) { observer.observe(el); });
    }

    /* ── 2. Number counter ([data-count-up]) ───────────────────────
       Usage:
         <span data-count-up="1234.50" data-count-prefix="Kshs ">0</span>

       Attributes:
         data-count-up      — target number (float or int)
         data-count-prefix  — string prepended to the value (e.g. "Kshs ")
         data-count-decimals— decimal places (default: auto-detected)
    ──────────────────────────────────────────────────────────────── */
    function initCounters() {
        const counters = document.querySelectorAll('[data-count-up]');
        if (!counters.length || typeof gsap === 'undefined') return;

        const observer = new IntersectionObserver(
            function (entries) {
                entries.forEach(function (entry) {
                    if (!entry.isIntersecting) return;

                    const el      = entry.target;
                    const target  = parseFloat(el.dataset.countUp)  || 0;
                    const prefix  = el.dataset.countPrefix           || '';
                    const rawDec  = el.dataset.countDecimals;
                    const decimals = rawDec !== undefined
                        ? parseInt(rawDec, 10)
                        : (target % 1 !== 0 ? 2 : 0);

                    const obj = { val: 0 };

                    gsap.to(obj, {
                        val     : target,
                        duration: 1.4,
                        ease    : 'power2.out',
                        onUpdate: function () {
                            el.textContent = prefix + obj.val.toFixed(decimals);
                        },
                        onComplete: function () {
                            /* Final value — ensure no floating-point drift */
                            el.textContent = prefix + target.toFixed(decimals);
                            el.classList.add('count-up-done');
                        }
                    });

                    observer.unobserve(el); // animate once
                });
            },
            { threshold: 0.3 }
        );

        counters.forEach(function (el) {
            /* Set initial display text to "0" or "0.00" */
            const target  = parseFloat(el.dataset.countUp) || 0;
            const rawDec  = el.dataset.countDecimals;
            const decimals = rawDec !== undefined
                ? parseInt(rawDec, 10)
                : (target % 1 !== 0 ? 2 : 0);
            const prefix  = el.dataset.countPrefix || '';
            el.textContent = prefix + (0).toFixed(decimals);

            observer.observe(el);
        });
    }

    /* ── Boot ───────────────────────────────────────────────────── */
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', function () {
            initScrollReveal();
            initCounters();
        });
    } else {
        initScrollReveal();
        initCounters();
    }
}());
