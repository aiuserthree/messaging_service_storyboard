/* ============================================================
   TOKBELL — Main JavaScript
   MOASHOT-style interactions: scroll animations, counters,
   marquee, header scroll, hamburger menu, smooth scroll
   ============================================================ */

document.addEventListener('DOMContentLoaded', function () {

    // ─── 1. SCROLL FADE-IN ANIMATIONS ────────────────────────
    const animEls = document.querySelectorAll('[data-animate]');

    const animObserver = new IntersectionObserver((entries) => {
        entries.forEach((entry) => {
            if (entry.isIntersecting) {
                // Stagger children within the same parent
                const parent = entry.target.closest('section') || entry.target.parentElement;
                const siblings = parent.querySelectorAll('[data-animate]:not(.visible)');
                
                let delay = 0;
                siblings.forEach((sib) => {
                    if (isInViewport(sib)) {
                        sib.style.transitionDelay = delay + 'ms';
                        sib.classList.add('visible');
                        delay += 150;
                        animObserver.unobserve(sib);
                    }
                });

                // Ensure the current entry is always marked
                if (!entry.target.classList.contains('visible')) {
                    entry.target.classList.add('visible');
                    animObserver.unobserve(entry.target);
                }
            }
        });
    }, {
        root: null,
        rootMargin: '0px 0px -40px 0px',
        threshold: 0.1
    });

    animEls.forEach((el) => animObserver.observe(el));

    function isInViewport(el) {
        const rect = el.getBoundingClientRect();
        return rect.top < window.innerHeight && rect.bottom > 0;
    }


    // ─── 2. HEADER SCROLL EFFECT ─────────────────────────────
    const siteHeader = document.getElementById('siteHeader')
        || document.querySelector('header.header');

    function handleHeaderScroll() {
        if (!siteHeader) return;
        if (window.scrollY > 80) {
            siteHeader.classList.add('scrolled');
        } else {
            siteHeader.classList.remove('scrolled');
        }
    }

    window.addEventListener('scroll', handleHeaderScroll, { passive: true });
    handleHeaderScroll();


    // ─── 3. HAMBURGER MENU ───────────────────────────────────
    const hamburgerBtn = document.getElementById('hamburgerBtn');
    const mobileOverlay = document.getElementById('mobileOverlay');

    if (hamburgerBtn && mobileOverlay) {
        hamburgerBtn.addEventListener('click', function () {
            hamburgerBtn.classList.toggle('active');
            mobileOverlay.classList.toggle('active');
            document.body.style.overflow = mobileOverlay.classList.contains('active') ? 'hidden' : '';
        });

        mobileOverlay.querySelectorAll('a').forEach(link => {
            link.addEventListener('click', () => {
                hamburgerBtn.classList.remove('active');
                mobileOverlay.classList.remove('active');
                document.body.style.overflow = '';
            });
        });
    }


    // ─── 4. SMOOTH SCROLL FOR ANCHOR LINKS ───────────────────
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            const targetId = this.getAttribute('href');
            if (targetId === '#') return;

            const targetEl = document.querySelector(targetId);
            if (targetEl) {
                e.preventDefault();
                const headerH = siteHeader ? siteHeader.offsetHeight : 72;
                const pos = targetEl.getBoundingClientRect().top + window.pageYOffset - headerH - 16;

                window.scrollTo({
                    top: pos,
                    behavior: 'smooth'
                });
            }
        });
    });


    // ─── 5. NUMBER COUNT-UP ANIMATION ────────────────────────
    // For integer counts (benefits section)
    const countEls = document.querySelectorAll('.benefit-value[data-count]');

    const countObserver = new IntersectionObserver((entries) => {
        entries.forEach((entry) => {
            if (entry.isIntersecting) {
                const el = entry.target;
                const target = parseInt(el.getAttribute('data-count'), 10);
                animateCount(el, 0, target, 1500, false);
                countObserver.unobserve(el);
            }
        });
    }, { threshold: 0.5 });

    countEls.forEach(el => countObserver.observe(el));


    // For decimal price counts (pricing section)
    const priceEls = document.querySelectorAll('.pc-number[data-count-decimal]');

    const priceObserver = new IntersectionObserver((entries) => {
        entries.forEach((entry) => {
            if (entry.isIntersecting) {
                const el = entry.target;
                const target = parseFloat(el.getAttribute('data-count-decimal'));
                const isDecimal = target % 1 !== 0;
                animateCount(el, 0, target, 1200, isDecimal);
                priceObserver.unobserve(el);
            }
        });
    }, { threshold: 0.5 });

    priceEls.forEach(el => priceObserver.observe(el));


    function animateCount(element, start, end, duration, isDecimal) {
        const startTime = performance.now();
        const decPlaces = isDecimal ? (end.toString().split('.')[1] || '').length : 0;

        function update(now) {
            const elapsed = now - startTime;
            const progress = Math.min(elapsed / duration, 1);

            // easeOutCubic
            const ease = 1 - Math.pow(1 - progress, 3);
            const current = start + (end - start) * ease;

            if (isDecimal) {
                element.textContent = current.toFixed(decPlaces);
            } else {
                // Format with comma for thousands
                element.textContent = Math.round(current).toLocaleString('ko-KR');
            }

            if (progress < 1) {
                requestAnimationFrame(update);
            }
        }

        requestAnimationFrame(update);
    }


    // ─── 6. ANALYTICS BAR ANIMATION (app showcase) ───────────
    const fanBars = document.querySelectorAll('.fan-bar');
    const appSection = document.querySelector('.app-showcase');

    if (appSection && fanBars.length > 0) {
        const barObserver = new IntersectionObserver((entries) => {
            entries.forEach((entry) => {
                if (entry.isIntersecting) {
                    fanBars.forEach((bar) => {
                        const w = bar.style.width;
                        bar.style.width = '0%';
                        bar.style.transition = 'width 1.2s ease';
                        setTimeout(() => {
                            bar.style.width = w;
                        }, 300);
                    });
                    barObserver.unobserve(entry.target);
                }
            });
        }, { threshold: 0.3 });

        barObserver.observe(appSection);
    }


    // ─── 7. ACTIVE NAV LINK ON SCROLL ────────────────────────
    const sections = document.querySelectorAll('section[id]');
    const navLinks = document.querySelectorAll('.header-nav .nav-link');

    function updateActiveNav() {
        if (!siteHeader || navLinks.length === 0) return;
        const scrollPos = window.scrollY + siteHeader.offsetHeight + 100;

        sections.forEach((section) => {
            const top = section.offsetTop;
            const height = section.offsetHeight;
            const id = section.getAttribute('id');

            if (scrollPos >= top && scrollPos < top + height) {
                navLinks.forEach(link => {
                    link.classList.remove('active');
                    if (link.getAttribute('href') === '#' + id) {
                        link.classList.add('active');
                    }
                });
            }
        });
    }

    window.addEventListener('scroll', updateActiveNav, { passive: true });

});
