/* ============================================================
   tokbell — Main JavaScript
   Scroll animations, header, hamburger, FAQ accordion, count-up
   ============================================================ */

document.addEventListener('DOMContentLoaded', function () {

    // ─── 1. SCROLL FADE-IN ANIMATIONS (stagger 200ms) ───────
    const animEls = document.querySelectorAll('[data-animate]');

    const animObserver = new IntersectionObserver((entries) => {
        entries.forEach((entry) => {
            if (entry.isIntersecting) {
                const parent = entry.target.parentElement;
                if (!parent) {
                    entry.target.classList.add('visible');
                    animObserver.unobserve(entry.target);
                    return;
                }

                const siblings = parent.querySelectorAll('[data-animate]:not(.visible)');
                let delay = 0;

                siblings.forEach((sib) => {
                    const rect = sib.getBoundingClientRect();
                    if (rect.top < window.innerHeight + 60) {
                        sib.style.transitionDelay = delay + 'ms';
                        sib.classList.add('visible');
                        delay += 200;
                        animObserver.unobserve(sib);
                    }
                });

                if (!entry.target.classList.contains('visible')) {
                    entry.target.classList.add('visible');
                    animObserver.unobserve(entry.target);
                }
            }
        });
    }, {
        root: null,
        rootMargin: '0px 0px -40px 0px',
        threshold: 0.08
    });

    animEls.forEach((el) => animObserver.observe(el));


    // ─── 2. HEADER SCROLL EFFECT (공통 GNB .header) ────────
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


    // ─── 3. HAMBURGER / MOBILE DRAWER ────────────────────────
    const hamburgerBtn = document.getElementById('hamburgerBtn');
    const mobileDrawer = document.getElementById('mobileDrawer');
    const drawerOverlay = document.getElementById('drawerOverlay');

    function openDrawer() {
        hamburgerBtn.classList.add('active');
        mobileDrawer.classList.add('active');
        drawerOverlay.classList.add('active');
        document.body.style.overflow = 'hidden';
    }

    function closeDrawer() {
        hamburgerBtn.classList.remove('active');
        mobileDrawer.classList.remove('active');
        drawerOverlay.classList.remove('active');
        document.body.style.overflow = '';
    }

    if (hamburgerBtn) {
        hamburgerBtn.addEventListener('click', function () {
            if (mobileDrawer.classList.contains('active')) {
                closeDrawer();
            } else {
                openDrawer();
            }
        });
    }

    if (drawerOverlay) {
        drawerOverlay.addEventListener('click', closeDrawer);
    }

    if (mobileDrawer) {
        mobileDrawer.querySelectorAll('a').forEach(link => {
            link.addEventListener('click', closeDrawer);
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
                const pos = targetEl.getBoundingClientRect().top + window.pageYOffset - headerH - 20;

                window.scrollTo({
                    top: pos,
                    behavior: 'smooth'
                });
            }
        });
    });


    // ─── 5. FAQ ACCORDION ────────────────────────────────────
    const faqItems = document.querySelectorAll('.faq-item');

    faqItems.forEach((item) => {
        const question = item.querySelector('.faq-question');
        if (!question) return;

        question.addEventListener('click', () => {
            const isActive = item.classList.contains('active');

            // Close all other items
            faqItems.forEach((other) => {
                if (other !== item) {
                    other.classList.remove('active');
                    const btn = other.querySelector('.faq-question');
                    if (btn) btn.setAttribute('aria-expanded', 'false');
                }
            });

            // Toggle current item
            if (isActive) {
                item.classList.remove('active');
                question.setAttribute('aria-expanded', 'false');
            } else {
                item.classList.add('active');
                question.setAttribute('aria-expanded', 'true');
            }
        });
    });


    // ─── 6. PRICE COUNT-UP ANIMATION ─────────────────────────
    const priceEls = document.querySelectorAll('[data-count]');

    if (priceEls.length > 0) {
        const priceObserver = new IntersectionObserver((entries) => {
            entries.forEach((entry) => {
                if (entry.isIntersecting) {
                    const el = entry.target;
                    const target = parseFloat(el.getAttribute('data-count'));
                    animateCountUp(el, 0, target, 1200);
                    priceObserver.unobserve(el);
                }
            });
        }, { threshold: 0.3 });

        priceEls.forEach((el) => priceObserver.observe(el));
    }

    // Promo count-up
    const promoCountEl = document.querySelector('[data-count-up]');
    if (promoCountEl) {
        const promoObserver = new IntersectionObserver((entries) => {
            entries.forEach((entry) => {
                if (entry.isIntersecting) {
                    const target = parseInt(entry.target.getAttribute('data-count-up'));
                    animateCountUp(entry.target, 0, target, 1500, true);
                    promoObserver.unobserve(entry.target);
                }
            });
        }, { threshold: 0.5 });

        promoObserver.observe(promoCountEl);
    }

    function animateCountUp(el, start, end, duration, isInteger) {
        const startTime = performance.now();
        const hasDecimal = !isInteger && String(end).includes('.');
        const decimalPlaces = hasDecimal ? String(end).split('.')[1].length : 0;

        function tick(now) {
            const elapsed = now - startTime;
            const progress = Math.min(elapsed / duration, 1);
            // Ease-out cubic
            const eased = 1 - Math.pow(1 - progress, 3);
            const current = start + (end - start) * eased;

            if (hasDecimal) {
                el.textContent = current.toFixed(decimalPlaces);
            } else {
                el.textContent = Math.round(current);
            }

            if (progress < 1) {
                requestAnimationFrame(tick);
            }
        }

        requestAnimationFrame(tick);
    }


    // ─── 7. CHART BAR ANIMATION ──────────────────────────────
    const chartBars = document.querySelectorAll('.chart-bar');

    if (chartBars.length > 0) {
        // Store target heights and set to 0
        chartBars.forEach((bar) => {
            bar.dataset.targetHeight = bar.style.height;
            bar.style.height = '0%';
        });

        const chartObserver = new IntersectionObserver((entries) => {
            entries.forEach((entry) => {
                if (entry.isIntersecting) {
                    const bars = entry.target.querySelectorAll('.chart-bar');
                    bars.forEach((bar, i) => {
                        setTimeout(() => {
                            bar.style.height = bar.dataset.targetHeight;
                        }, i * 200);
                    });
                    chartObserver.unobserve(entry.target);
                }
            });
        }, { threshold: 0.3 });

        const chartContainer = document.querySelector('.mockup-chart');
        if (chartContainer) chartObserver.observe(chartContainer);
    }


    // ─── 8. ACTIVE NAV LINK (구 GNB 앵커용 — 공통 헤더에서는 미사용) ─
    const sections = document.querySelectorAll('.landing-v12 section[id]');
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

    if (navLinks.length > 0) {
        window.addEventListener('scroll', updateActiveNav, { passive: true });
    }

});
