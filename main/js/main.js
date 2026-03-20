/* ============================================================
   톡벨 — Main JavaScript
   Scroll animations, navigation, interactions
   ============================================================ */

document.addEventListener('DOMContentLoaded', function () {

    // === Scroll-based animations (Intersection Observer) ===
    const animatedElements = document.querySelectorAll('[data-animate]');

    const observerOptions = {
        root: null,
        rootMargin: '0px 0px -60px 0px',
        threshold: 0.15
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach((entry) => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    animatedElements.forEach((el, index) => {
        // Stagger animation delays
        el.style.transitionDelay = `${index * 0.05}s`;
        observer.observe(el);
    });


    // === Navbar shadow on scroll (main/index 전용 nav; index.html은 사이트 GNB만 사용 시 없을 수 있음) ===
    const navHeader = document.getElementById('navHeader');

    function handleNavScroll() {
        if (!navHeader) return;
        if (window.scrollY > 10) {
            navHeader.classList.add('scrolled');
        } else {
            navHeader.classList.remove('scrolled');
        }
    }

    if (navHeader) {
        window.addEventListener('scroll', handleNavScroll, { passive: true });
        handleNavScroll();
    }


    // === Mobile menu toggle ===
    const mobileToggle = document.getElementById('mobileToggle');
    const mobileMenu = document.getElementById('mobileMenu');

    if (mobileToggle && mobileMenu) {
        mobileToggle.addEventListener('click', function () {
            mobileMenu.classList.toggle('active');
            
            // Animate hamburger to X
            const spans = mobileToggle.querySelectorAll('span');
            if (mobileMenu.classList.contains('active')) {
                spans[0].style.transform = 'rotate(45deg) translate(5px, 5px)';
                spans[1].style.opacity = '0';
                spans[2].style.transform = 'rotate(-45deg) translate(5px, -5px)';
            } else {
                spans[0].style.transform = 'none';
                spans[1].style.opacity = '1';
                spans[2].style.transform = 'none';
            }
        });

        // Close mobile menu when clicking a link
        mobileMenu.querySelectorAll('a').forEach(link => {
            link.addEventListener('click', () => {
                mobileMenu.classList.remove('active');
                const spans = mobileToggle.querySelectorAll('span');
                spans[0].style.transform = 'none';
                spans[1].style.opacity = '1';
                spans[2].style.transform = 'none';
            });
        });
    }


    // === Smooth scroll for anchor links ===
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            const targetId = this.getAttribute('href');
            if (targetId === '#') return;

            const targetEl = document.querySelector(targetId);
            if (targetEl) {
                e.preventDefault();
                const navHeight = navHeader ? navHeader.offsetHeight : 72;
                const targetPosition = targetEl.getBoundingClientRect().top + window.pageYOffset - navHeight - 20;

                window.scrollTo({
                    top: targetPosition,
                    behavior: 'smooth'
                });
            }
        });
    });


    // === Analytics bar animation on scroll ===
    const barFills = document.querySelectorAll('.bar-fill');
    const analyticsCard = document.querySelector('.analytics-card');

    if (analyticsCard && barFills.length > 0) {
        const barObserver = new IntersectionObserver((entries) => {
            entries.forEach((entry) => {
                if (entry.isIntersecting) {
                    barFills.forEach((bar) => {
                        const width = bar.style.width;
                        bar.style.width = '0%';
                        setTimeout(() => {
                            bar.style.width = width;
                        }, 200);
                    });
                    barObserver.unobserve(entry.target);
                }
            });
        }, { threshold: 0.3 });

        barObserver.observe(analyticsCard);
    }


    // === Counter animation for pricing numbers ===
    const priceNumbers = document.querySelectorAll('.price-number');

    const counterObserver = new IntersectionObserver((entries) => {
        entries.forEach((entry) => {
            if (entry.isIntersecting) {
                const el = entry.target;
                const finalValue = parseFloat(el.textContent);
                animateCounter(el, 0, finalValue, 1200);
                counterObserver.unobserve(el);
            }
        });
    }, { threshold: 0.5 });

    priceNumbers.forEach(el => counterObserver.observe(el));

    function animateCounter(element, start, end, duration) {
        const startTime = performance.now();
        const isDecimal = end % 1 !== 0;
        const decimalPlaces = isDecimal ? (end.toString().split('.')[1] || '').length : 0;

        function update(currentTime) {
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / duration, 1);

            // Ease out cubic
            const easeOut = 1 - Math.pow(1 - progress, 3);
            const current = start + (end - start) * easeOut;

            if (isDecimal) {
                element.textContent = current.toFixed(decimalPlaces);
            } else {
                element.textContent = Math.round(current);
            }

            if (progress < 1) {
                requestAnimationFrame(update);
            }
        }

        requestAnimationFrame(update);
    }

});
