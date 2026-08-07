/**
 * MerryChama — Modal / Dialog System
 * Phase 7: Open/close logic, keyboard handling, focus trap, backdrop click.
 * Loaded per-page via {% static 'js/modals.js' %}
 */

(function () {
    'use strict';

    /* ── Open a modal ─────────────────────────────────────────────── */
    function openModal(id) {
        const backdrop = document.getElementById(id);
        if (!backdrop) return;

        backdrop.classList.add('is-open');
        backdrop.removeAttribute('aria-hidden');

        /* Move focus to the first focusable element inside the dialog */
        const focusable = backdrop.querySelectorAll(
            'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
        );
        if (focusable.length) focusable[0].focus();

        /* Prevent body scroll */
        document.body.style.overflow = 'hidden';
    }

    /* ── Close a modal ────────────────────────────────────────────── */
    function closeModal(id) {
        const backdrop = document.getElementById(id);
        if (!backdrop) return;

        backdrop.classList.remove('is-open');
        backdrop.setAttribute('aria-hidden', 'true');

        document.body.style.overflow = '';
    }

    /* ── Escape key closes the topmost open modal ─────────────────── */
    document.addEventListener('keydown', function (e) {
        if (e.key !== 'Escape') return;
        const open = document.querySelector('.modal-backdrop.is-open');
        if (open) closeModal(open.id);
    });

    /* ── Backdrop click closes the modal ─────────────────────────── */
    document.addEventListener('click', function (e) {
        if (e.target.classList.contains('modal-backdrop')) {
            closeModal(e.target.id);
        }
    });

    /* ── Expose globally ──────────────────────────────────────────── */
    window.openModal  = openModal;
    window.closeModal = closeModal;
}());
