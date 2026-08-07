/**
 * MerryChama — Magnet Effect
 * Vanilla JS port of the React Bits <Magnet /> component.
 * Loaded by home.html via {% static 'js/magnet.js' %}
 *
 * Usage — add data attributes to your wrapper element:
 *   <span id="magnet-wrapper" data-magnet-target="hero-cta"
 *         data-padding="60" data-strength="4">
 *     <a id="hero-cta" ...>Click me</a>
 *   </span>
 *
 * Or call initMagnet() manually after the DOM is ready.
 */

(function () {
    function initMagnet({
        wrapperId  = 'magnet-wrapper',
        innerId    = 'hero-cta',
        padding    = 60,
        strength   = 4,
        activeTr   = 'transform 0.3s ease-out',
        inactiveTr = 'transform 0.5s ease-in-out',
    } = {}) {
        const wrapper = document.getElementById(wrapperId);
        const inner   = document.getElementById(innerId);
        if (!wrapper || !inner) return;

        let active = false;

        window.addEventListener('mousemove', function (e) {
            const rect    = wrapper.getBoundingClientRect();
            const centerX = rect.left + rect.width  / 2;
            const centerY = rect.top  + rect.height / 2;
            const distX   = Math.abs(centerX - e.clientX);
            const distY   = Math.abs(centerY - e.clientY);

            if (distX < rect.width / 2 + padding && distY < rect.height / 2 + padding) {
                if (!active) {
                    active = true;
                    inner.style.transition = activeTr;
                }
                const offsetX = (e.clientX - centerX) / strength;
                const offsetY = (e.clientY - centerY) / strength;
                inner.style.transform = `translate3d(${offsetX}px, ${offsetY}px, 0)`;
            } else {
                if (active) {
                    active = false;
                    inner.style.transition = inactiveTr;
                    inner.style.transform  = 'translate3d(0, 0, 0)';
                }
            }
        });
    }

    /* Auto-init if the wrapper element is on the page */
    document.addEventListener('DOMContentLoaded', () => initMagnet());

    /* Also expose globally so pages can call it with custom options */
    window.initMagnet = initMagnet;
}());
