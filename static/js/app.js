/**
 * ChamaFlow — Shared UI Behaviors
 * Ported from merry_chama2/static/js/app.js — no framework, no build step.
 * Loaded globally in base.html (defer).
 */

/* ── Theme toggle ───────────────────────────────────────────────────
   Enables / disables theme.css (the dark stylesheet) and persists
   the user's choice to localStorage. The FOUC prevention script in
   base.html applies the saved preference before paint.
────────────────────────────────────────────────────────────────── */
window.cfToggleTheme = function () {
    var link = document.getElementById('theme-stylesheet');
    if (!link) return;

    /* If the sheet is currently active (dark mode), disable it → light mode */
    var goingLight = !link.disabled;
    link.disabled = goingLight;
    localStorage.setItem('cf-theme', goingLight ? 'light' : 'dark');

    /* Swap icon: sun = "click to go light", moon = "click to go dark" */
    var icon = goingLight ? 'fa-moon' : 'fa-sun';
    document.querySelectorAll('[data-theme-icon]').forEach(function (el) {
        el.classList.remove('fa-moon', 'fa-sun');
        el.classList.add(icon);
    });
};

/* Sync icon with saved theme on every page load */
document.addEventListener('DOMContentLoaded', function () {
    var link   = document.getElementById('theme-stylesheet');
    var isDark = link && !link.disabled;            /* disabled = light mode */
    var icon   = isDark ? 'fa-sun' : 'fa-moon';    /* sun while dark, moon while light */
    document.querySelectorAll('[data-theme-icon]').forEach(function (el) {
        el.classList.remove('fa-moon', 'fa-sun');
        el.classList.add(icon);
    });
});

/* ── cfToast — JS-triggered toast messages ──────────────────────── */
window.cfToast = function (text, type, timeout) {
    type    = type    || 'info';
    timeout = timeout || 4500;

    const region = document.getElementById('toast-region');
    if (!region) return;

    const icons = {
        success : 'fa-circle-check',
        error   : 'fa-circle-exclamation',
        warning : 'fa-triangle-exclamation',
        info    : 'fa-circle-info'
    };

    const el = document.createElement('div');
    el.className = 'toast toast-' + type;
    el.setAttribute('role', 'status');
    el.innerHTML =
        '<i class="fa-solid ' + (icons[type] || icons.info) + ' toast-icon"></i>' +
        '<span style="flex:1">' + text + '</span>' +
        '<button aria-label="Dismiss" onclick="this.closest(\'.toast\').remove()" style="color:inherit;opacity:.6;background:none;border:none;cursor:pointer;padding:0;line-height:1;">' +
            '<i class="fa-solid fa-xmark"></i>' +
        '</button>';

    region.appendChild(el);

    setTimeout(function () {
        el.classList.add('is-leaving');
        setTimeout(function () { el.remove(); }, 220);
    }, timeout);
};

/* ── Loading button state ────────────────────────────────────────── */
function cfSetLoading(btn) {
    if (!btn) return;
    btn.classList.add('is-loading');
    btn.disabled = true;
}

document.addEventListener('DOMContentLoaded', function () {
    /* Regular forms (not modals) auto-set loading state on submit */
    document.querySelectorAll('form:not([data-no-loading])').forEach(function (form) {
        form.addEventListener('submit', function () {
            cfSetLoading(form.querySelector('button[type="submit"]'));
        });
    });
});

/* ── Spotlight cards — radial glow follows cursor ────────────────── */
document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.card-spotlight').forEach(function (card) {
        card.addEventListener('mousemove', function (e) {
            const rect = card.getBoundingClientRect();
            card.style.setProperty('--spot-x', (e.clientX - rect.left) + 'px');
            card.style.setProperty('--spot-y', (e.clientY - rect.top)  + 'px');
        });
    });
});

/* ── cfCopy — clipboard utility (for invite codes etc.) ─────────── */
window.cfCopy = function (text, btn) {
    if (!navigator.clipboard) return;
    navigator.clipboard.writeText(text).then(function () {
        cfToast('Copied to clipboard', 'success', 2000);
        if (btn) {
            const original = btn.innerHTML;
            btn.innerHTML = '<i class="fa-solid fa-check"></i>';
            setTimeout(function () { btn.innerHTML = original; }, 1200);
        }
    });
};

/* ── cfTableSearch — live client-side table filter ──────────────── */
window.cfTableSearch = function (inputEl, tableBodyId, emptyStateId) {
    const q      = inputEl.value.trim().toLowerCase();
    const tbody  = document.getElementById(tableBodyId);
    if (!tbody) return;

    let visible = 0;
    tbody.querySelectorAll('tr[data-row]').forEach(function (row) {
        const match = row.textContent.toLowerCase().includes(q);
        row.style.display = match ? '' : 'none';
        if (match) visible += 1;
    });

    const emptyEl = emptyStateId ? document.getElementById(emptyStateId) : null;
    if (emptyEl) emptyEl.style.display = (visible === 0) ? '' : 'none';
};
