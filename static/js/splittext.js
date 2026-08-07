/**
 * ChamaFlow — SplitText
 * Vanilla JS port of the React Bits SplitText component.
 * Loaded by base.html via {% static 'js/splittext.js' %}
 *
 * Usage:
 *   SplitText('#my-el', {
 *     splitType: 'chars',          // 'chars' | 'words'
 *     delay: 60,                   // stagger delay in ms
 *     duration: 0.8,
 *     ease: 'power3.out',
 *     from: { opacity: 0, y: 40 },
 *     to:   { opacity: 1, y: 0 },
 *     threshold: 0.1,
 *     rootMargin: '-100px',
 *     textAlign: 'center',
 *     onLetterAnimationComplete: () => {}
 *   });
 */

gsap.registerPlugin(ScrollTrigger);

function SplitText(selector, {
    delay                    = 50,
    duration                 = 1.25,
    ease                     = 'power3.out',
    splitType                = 'chars',
    from                     = { opacity: 0, y: 40 },
    to                       = { opacity: 1, y: 0 },
    threshold                = 0.1,
    rootMargin               = '-100px',
    textAlign                = 'center',
    onLetterAnimationComplete = null
} = {}) {
    const el = typeof selector === 'string'
        ? document.querySelector(selector)
        : selector;
    if (!el) return;

    /* ── Split the DOM ──────────────────────────────────────────── */
    const rawText = el.textContent;
    el.innerHTML  = '';
    el.style.textAlign = textAlign;

    const targets   = [];
    const wantChars = splitType.includes('chars');

    const words = rawText.split(/(\s+)/);   // keep whitespace tokens
    words.forEach(token => {
        if (/^\s+$/.test(token)) {
            el.appendChild(document.createTextNode(token));
            return;
        }
        if (wantChars) {
            const wordWrap = document.createElement('span');
            wordWrap.className = 'split-word';
            token.split('').forEach(ch => {
                const span = document.createElement('span');
                span.className   = 'split-char';
                span.textContent = ch;
                wordWrap.appendChild(span);
                targets.push(span);
            });
            el.appendChild(wordWrap);
        } else {
            const span = document.createElement('span');
            span.className   = 'split-word';
            span.textContent = token;
            el.appendChild(span);
            targets.push(span);
        }
    });

    /* ── Build ScrollTrigger start string ───────────────────────── */
    const startPct = (1 - threshold) * 100;
    const m        = /^(-?\d+(?:\.\d+)?)(px|em|rem|%)?$/.exec(rootMargin.trim());
    const mVal     = m ? parseFloat(m[1]) : 0;
    const mUnit    = m ? (m[2] || 'px') : 'px';
    const offset   = mVal === 0 ? ''
                   : mVal < 0  ? ` -=${Math.abs(mVal)}${mUnit}`
                                : ` +=${mVal}${mUnit}`;
    const start    = `top ${startPct}%${offset}`;

    /* ── Animate ────────────────────────────────────────────────── */
    gsap.fromTo(
        targets,
        { ...from },
        {
            ...to,
            duration,
            ease,
            stagger: delay / 1000,
            force3D: true,
            scrollTrigger: {
                trigger: el,
                start,
                once: true,
                fastScrollEnd: true
            },
            onComplete: () => {
                if (typeof onLetterAnimationComplete === 'function')
                    onLetterAnimationComplete();
            }
        }
    );
}
