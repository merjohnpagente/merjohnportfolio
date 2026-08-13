document.addEventListener('DOMContentLoaded', () => {

    /* ========== LENIS SMOOTH SCROLL ========== */
    const lenis = new Lenis({
        duration: 1.2,
        easing: (t) => Math.min(1, 1.001 - Math.pow(2, -10 * t)),
        smoothWheel: true,
    });

    function raf(time) {
        lenis.raf(time);
        requestAnimationFrame(raf);
    }
    requestAnimationFrame(raf);

    /* ========== YEAR ========== */
    const yearEl = document.getElementById('year');
    if (yearEl) yearEl.textContent = new Date().getFullYear();

    /* ========== MOBILE MENU ========== */
    const menuToggle = document.getElementById('menuToggle');
    const mobileNav = document.getElementById('mobileNav');
    if (menuToggle && mobileNav) {
        menuToggle.addEventListener('click', () => {
            const isOpen = mobileNav.classList.toggle('is-open');
            menuToggle.setAttribute('aria-expanded', isOpen);
        });
        mobileNav.querySelectorAll('a').forEach(a => {
            a.addEventListener('click', () => {
                mobileNav.classList.remove('is-open');
                menuToggle.setAttribute('aria-expanded', 'false');
            });
        });
    }

    /* ========== SMOOTH ANCHOR SCROLL ========== */
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            const targetId = this.getAttribute('href');
            if (targetId === '#' || targetId === '#!') return;
            const target = document.querySelector(targetId);
            if (target) {
                e.preventDefault();
                lenis.scrollTo(target);
            }
        });
    });

    /* ========== PROGRESS BAR ========== */
    const progressFill = document.getElementById('progressFill');
    function updateProgress() {
        if (!progressFill) return;
        const docHeight = document.documentElement.scrollHeight - window.innerHeight;
        const progress = docHeight > 0 ? (window.scrollY / docHeight) * 100 : 0;
        progressFill.style.width = `${Math.min(progress, 100)}%`;
    }
    window.addEventListener('scroll', updateProgress, { passive: true });

    /* ========== CURSOR GLOW ========== */
    const cursorGlow = document.getElementById('cursorGlow');
    if (cursorGlow) {
        document.addEventListener('mousemove', (e) => {
            cursorGlow.style.opacity = '1';
            cursorGlow.style.left = e.clientX + 'px';
            cursorGlow.style.top = e.clientY + 'px';
        });
        document.addEventListener('mouseleave', () => { cursorGlow.style.opacity = '0'; });
        document.addEventListener('mouseenter', () => { cursorGlow.style.opacity = '1'; });
    }

    /* ========== TYPING EFFECT ========== */
    const heroSub = document.getElementById('heroSub');
    if (heroSub) {
        const words = ['Web Developer · UI/UX Designer · Front-End Specialist'];
        let charIndex = 0;
        const word = words[0];

        function typeLoop() {
            if (charIndex < word.length) {
                heroSub.textContent = word.substring(0, charIndex + 1);
                charIndex++;
                setTimeout(typeLoop, 50);
            }
        }
        setTimeout(typeLoop, 300);
    }

    /* ========== SCROLL REVEAL ========== */
    const revealEls = document.querySelectorAll('[data-reveal], [data-reveal-img]');
    function revealOnScroll() {
        const windowH = window.innerHeight;
        revealEls.forEach(el => {
            const top = el.getBoundingClientRect().top;
            if (top < windowH - 60) {
                el.style.opacity = '1';
                el.style.transform = 'translateY(0)';
            }
        });
    }
    window.addEventListener('scroll', revealOnScroll, { passive: true });
    revealOnScroll();

    /* ========== COUNTER ANIMATION ========== */
    const statNumbers = document.querySelectorAll('.stat-number[data-count]');
    function animateCounters() {
        statNumbers.forEach(el => {
            const rect = el.getBoundingClientRect();
            if (rect.top < window.innerHeight - 80 && !el.dataset.done) {
                el.dataset.done = 'true';
                const target = parseInt(el.dataset.count);
                const duration = 2000;
                const start = performance.now();

                function update(now) {
                    const elapsed = now - start;
                    const progress = Math.min(elapsed / duration, 1);
                    const eased = 1 - Math.pow(1 - progress, 3);
                    el.textContent = target === 100
                        ? Math.floor(eased * target) + '%'
                        : Math.floor(eased * target);
                    if (progress < 1) requestAnimationFrame(update);
                }
                requestAnimationFrame(update);
            }
        });
    }
    window.addEventListener('scroll', animateCounters, { passive: true });
    animateCounters();

    /* ========== SKILL RING ANIMATION ========== */
    const skillRings = document.querySelectorAll('.ring-fill');
    function animateSkillRings() {
        skillRings.forEach(ring => {
            const rect = ring.closest('.skill-card').getBoundingClientRect();
            if (rect.top < window.innerHeight - 60 && !ring.dataset.done) {
                ring.dataset.done = 'true';
                const percent = parseInt(ring.dataset.percent);
                const svgEl = ring.closest('svg');
                const r = parseFloat(ring.getAttribute('r')) || 52;
                const circumference = 2 * Math.PI * r;
                const offset = circumference - (percent / 100) * circumference;
                ring.style.strokeDasharray = circumference;
                ring.style.strokeDashoffset = offset;
            }
        });
    }
    window.addEventListener('scroll', animateSkillRings, { passive: true });
    animateSkillRings();

    /* ========== WORK FILTER ========== */
    const filterBtns = document.querySelectorAll('.filter-btn');
    const workCards = document.querySelectorAll('.work-card');

    filterBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            filterBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            const filter = btn.dataset.filter;

            workCards.forEach(card => {
                if (filter === 'all' || card.dataset.category === filter) {
                    card.classList.remove('hidden');
                } else {
                    card.classList.add('hidden');
                }
            });
        });
    });

    /* ========== TILT EFFECT ========== */
    const tiltEls = document.querySelectorAll('[data-tilt]');

    tiltEls.forEach(el => {
        el.addEventListener('mousemove', (e) => {
            if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
            const rect = el.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            const centerX = rect.width / 2;
            const centerY = rect.height / 2;
            const rotateX = ((y - centerY) / centerY) * -5;
            const rotateY = ((x - centerX) / centerX) * 5;
            el.style.transform = `perspective(800px) rotateX(${rotateX}deg) rotateY(${rotateY}deg)`;
        });

        el.addEventListener('mouseleave', () => {
            el.style.transform = 'perspective(800px) rotateX(0deg) rotateY(0deg)';
        });
    });

    /* ========== PARALLAX (DATA-SPEED) ========== */
    const parallaxEls = document.querySelectorAll('[data-speed]');
    function updateParallax() {
        parallaxEls.forEach(el => {
            const speed = parseFloat(el.dataset.speed);
            const scrollY = window.scrollY;
            const offset = scrollY * speed;
            el.style.transform = `translateY(${offset}px)`;
        });
    }
    window.addEventListener('scroll', updateParallax, { passive: true });

    /* ========== ACTIVE NAV ON SCROLL ========== */
    const sections = document.querySelectorAll('section[id]');
    const navLinks = document.querySelectorAll('.site-nav a, .header-social a');

    function setActiveNav() {
        let scrollPos = window.scrollY + 150;
        sections.forEach(section => {
            const top = section.offsetTop - 120;
            const bottom = top + section.offsetHeight;
            if (scrollPos >= top && scrollPos < bottom) {
                navLinks.forEach(link => {
                    if (link.getAttribute('href') === '#' + section.id) {
                        navLinks.forEach(l => l.style.color = '');
                        link.style.color = 'var(--gold-bright)';
                    }
                });
            }
        });
    }
    window.addEventListener('scroll', setActiveNav, { passive: true });

    /* ========== DOWNLOAD RESUME ========== */
    const downloadResume = document.getElementById('downloadResume');
    if (downloadResume) {
        downloadResume.addEventListener('click', (e) => {
            e.preventDefault();
            const url = downloadResume.getAttribute('href');
            const filename = downloadResume.getAttribute('download') || 'resume.pdf';
            fetch(url)
                .then((res) => {
                    if (!res.ok) throw new Error('not found');
                    return res.blob();
                })
                .then((blob) => {
                    const objectUrl = URL.createObjectURL(blob);
                    const a = document.createElement('a');
                    a.href = objectUrl;
                    a.download = filename;
                    document.body.appendChild(a);
                    a.click();
                    a.remove();
                    URL.revokeObjectURL(objectUrl);
                })
                .catch(() => {
                    window.location.href = url;
                });
        });
    }

});