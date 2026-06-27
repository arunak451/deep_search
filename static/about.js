/* ============================================
   XPLORE IT CORP - ABOUT PAGE SCRIPTS
   Premium Interactions & Animations
   ============================================ */

document.addEventListener('DOMContentLoaded', () => {

    // ===== Background Particles =====
    const particleContainer = document.getElementById('bgParticles');
    const particleColors = ['#6c5ce7', '#00cec9', '#fd79a8', '#0984e3', '#00b894', '#f39c12'];

    function createParticles() {
        for (let i = 0; i < 40; i++) {
            const particle = document.createElement('div');
            particle.classList.add('particle');
            const size = Math.random() * 6 + 2;
            const color = particleColors[Math.floor(Math.random() * particleColors.length)];
            particle.style.cssText = `
                width: ${size}px;
                height: ${size}px;
                background: ${color};
                left: ${Math.random() * 100}%;
                animation-duration: ${Math.random() * 20 + 15}s;
                animation-delay: ${Math.random() * 10}s;
            `;
            particleContainer.appendChild(particle);
        }
    }
    createParticles();

    // ===== Navbar Scroll Effect =====
    const navbar = document.getElementById('navbar');
    let lastScroll = 0;

    window.addEventListener('scroll', () => {
        const currentScroll = window.pageYOffset;
        if (currentScroll > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
        lastScroll = currentScroll;
    });

    // ===== Active Nav Link on Scroll =====
    const sections = document.querySelectorAll('.section, .hero');
    const navLinks = document.querySelectorAll('.nav-link');

    const observerOptions = {
        root: null,
        rootMargin: '-20% 0px -60% 0px',
        threshold: 0,
    };

    const sectionObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const id = entry.target.id;
                navLinks.forEach(link => {
                    link.classList.remove('active');
                    if (link.getAttribute('href') === `#${id}`) {
                        link.classList.add('active');
                    }
                });
            }
        });
    }, observerOptions);

    sections.forEach(section => sectionObserver.observe(section));

    // ===== Mobile Menu =====
    const mobileMenuBtn = document.getElementById('mobileMenuBtn');
    const mobileMenu = document.getElementById('mobileMenu');
    const mobileLinks = document.querySelectorAll('.mobile-link');

    if (mobileMenuBtn) {
        mobileMenuBtn.addEventListener('click', () => {
            mobileMenu.classList.toggle('active');
            document.body.style.overflow = mobileMenu.classList.contains('active') ? 'hidden' : '';
        });

        mobileLinks.forEach(link => {
            link.addEventListener('click', () => {
                mobileMenu.classList.remove('active');
                document.body.style.overflow = '';
            });
        });
    }

    // ===== Floating Action Button (FAB) =====
    const fabMain = document.getElementById('fabMain');
    const fabContainer = document.getElementById('fabContainer');

    if (fabMain) {
        fabMain.addEventListener('click', () => {
            fabContainer.classList.toggle('active');
            fabMain.classList.toggle('active');
        });
    }

    // Close FAB when clicking outside
    document.addEventListener('click', (e) => {
        if (fabContainer && !fabContainer.contains(e.target)) {
            fabContainer.classList.remove('active');
            fabMain.classList.remove('active');
        }
    });

    // ===== Animated Number Counter =====
    const statNumbers = document.querySelectorAll('.stat-number');

    function animateCounter(el) {
        const target = parseFloat(el.dataset.target);
        const isDecimal = target % 1 !== 0;
        const duration = 2000;
        const startTime = performance.now();

        function update(currentTime) {
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / duration, 1);
            const easeOut = 1 - Math.pow(1 - progress, 3);
            const current = target * easeOut;

            if (isDecimal) {
                el.textContent = current.toFixed(1);
            } else {
                el.textContent = Math.floor(current).toLocaleString();
            }

            if (progress < 1) {
                requestAnimationFrame(update);
            }
        }

        requestAnimationFrame(update);
    }

    const counterObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                animateCounter(entry.target);
                counterObserver.unobserve(entry.target);
            }
        });
    }, { threshold: 0.5 });

    statNumbers.forEach(num => counterObserver.observe(num));

    // ===== Scroll Reveal Animation =====
    const revealElements = document.querySelectorAll(
        '.about-card, .service-card, .stat-card, .course-card, .contact-card, .section-header, .about-action-bar, .services-cta, .stats-buttons, .courses-actions, .team-actions, .social-section, .contact-form-wrap'
    );

    const revealObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
                revealObserver.unobserve(entry.target);
            }
        });
    }, { threshold: 0.1, rootMargin: '0px 0px -50px 0px' });

    revealElements.forEach((el, index) => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(40px)';
        el.style.transition = `opacity 0.6s ease ${index % 6 * 0.1}s, transform 0.6s ease ${index % 6 * 0.1}s`;
        revealObserver.observe(el);
    });

    // ===== Course Filter =====
    const filterBtns = document.querySelectorAll('.btn-filter');
    const courseCards = document.querySelectorAll('.course-card');

    filterBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            filterBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');

            const filter = btn.dataset.filter;
            courseCards.forEach(card => {
                if (filter === 'all' || card.dataset.category === filter) {
                    card.style.display = 'block';
                    card.style.animation = 'fadeInUp 0.5s ease forwards';
                } else {
                    card.style.display = 'none';
                }
            });
        });
    });

    // ===== Button Ripple Effect =====
    document.querySelectorAll('.btn').forEach(btn => {
        btn.addEventListener('click', function(e) {
            const ripple = document.createElement('span');
            const rect = this.getBoundingClientRect();
            const size = Math.max(rect.width, rect.height);
            const x = e.clientX - rect.left - size / 2;
            const y = e.clientY - rect.top - size / 2;

            ripple.style.cssText = `
                position: absolute;
                width: ${size}px;
                height: ${size}px;
                left: ${x}px;
                top: ${y}px;
                background: rgba(255, 255, 255, 0.15);
                border-radius: 50%;
                transform: scale(0);
                animation: rippleEffect 0.6s ease forwards;
                pointer-events: none;
                z-index: 10;
            `;

            this.appendChild(ripple);
            setTimeout(() => ripple.remove(), 600);
        });
    });

    // Add ripple keyframes
    const rippleStyle = document.createElement('style');
    rippleStyle.textContent = `
        @keyframes rippleEffect {
            to { transform: scale(4); opacity: 0; }
        }
    `;
    document.head.appendChild(rippleStyle);

    // ===== Magnetic Button Effect =====
    document.querySelectorAll('.btn-magnetic').forEach(btn => {
        btn.addEventListener('mousemove', (e) => {
            const rect = btn.getBoundingClientRect();
            const x = e.clientX - rect.left - rect.width / 2;
            const y = e.clientY - rect.top - rect.height / 2;
            btn.style.transform = `translate(${x * 0.15}px, ${y * 0.15}px)`;
        });

        btn.addEventListener('mouseleave', () => {
            btn.style.transform = 'translate(0, 0)';
        });
    });

    // ===== Smooth Scroll for Nav Links =====
    document.querySelectorAll('a[href^="#"]').forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const target = document.querySelector(link.getAttribute('href'));
            if (target) {
                target.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }
        });
    });

    // ===== Back to Top Button =====
    const btnBackToTop = document.getElementById('btnBackToTop');
    if (btnBackToTop) {
        btnBackToTop.addEventListener('click', () => {
            window.scrollTo({ top: 0, behavior: 'smooth' });
        });
    }

    // ===== Contact Form =====
    const contactForm = document.getElementById('contactForm');
    if (contactForm) {
        contactForm.addEventListener('submit', (e) => {
            e.preventDefault();
            
            const submitBtn = document.getElementById('btnSubmitForm');
            const originalContent = submitBtn.innerHTML;
            submitBtn.innerHTML = '<i class="fas fa-check-circle"></i> Message Sent!';
            submitBtn.style.background = 'linear-gradient(135deg, #00b894, #00cec9)';
            
            setTimeout(() => {
                submitBtn.innerHTML = originalContent;
                submitBtn.style.background = '';
                contactForm.reset();
            }, 3000);
        });
    }

    // ===== WhatsApp Button =====
    const whatsAppBtns = [
        document.getElementById('btnWhatsApp'),
        document.getElementById('fabWhatsApp')
    ];
    whatsAppBtns.forEach(btn => {
        if (btn) {
            btn.addEventListener('click', () => {
                window.open('https://wa.me/919047020807?text=Hi%20Xplore%20IT%20Corp!%20I%20am%20interested%20in%20your%20courses.', '_blank');
            });
        }
    });

    // ===== Call Button =====
    const callBtns = [
        document.getElementById('btnCallNow'),
        document.getElementById('fabCall')
    ];
    callBtns.forEach(btn => {
        if (btn) {
            btn.addEventListener('click', () => {
                window.open('tel:+919047020807');
            });
        }
    });

    // ===== Email Button =====
    const emailBtns = [
        document.getElementById('btnEmailUs'),
        document.getElementById('fabEmail')
    ];
    emailBtns.forEach(btn => {
        if (btn) {
            btn.addEventListener('click', () => {
                window.open('mailto:info@xploreitcorp.com');
            });
        }
    });

    // ===== Directions Button =====
    const btnDirections = document.getElementById('btnDirections');
    if (btnDirections) {
        btnDirections.addEventListener('click', () => {
            window.open('https://maps.google.com/?q=Xplore+IT+Corp+Coimbatore', '_blank');
        });
    }

    // ===== Visit Site Button =====
    const btnVisitSite = document.getElementById('btnVisitSite');
    if (btnVisitSite) {
        btnVisitSite.addEventListener('click', () => {
            window.open('http://www.xploreitcorp.com/', '_blank');
        });
    }

    // ===== Toast Notification System =====
    function showToast(message, icon = 'info-circle', type = 'info') {
        const toast = document.createElement('div');
        const colors = {
            info: 'linear-gradient(135deg, #6c5ce7, #0984e3)',
            success: 'linear-gradient(135deg, #00b894, #00cec9)',
            warning: 'linear-gradient(135deg, #f39c12, #e84393)'
        };

        toast.style.cssText = `
            position: fixed;
            top: 90px;
            right: 30px;
            background: ${colors[type]};
            color: white;
            padding: 16px 28px;
            border-radius: 12px;
            font-family: 'Outfit', sans-serif;
            font-size: 0.95rem;
            font-weight: 500;
            display: flex;
            align-items: center;
            gap: 12px;
            z-index: 10000;
            box-shadow: 0 8px 30px rgba(0,0,0,0.4);
            transform: translateX(120%);
            transition: transform 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
            max-width: 400px;
        `;

        toast.innerHTML = `<i class="fas fa-${icon}"></i> ${message}`;
        document.body.appendChild(toast);

        requestAnimationFrame(() => {
            toast.style.transform = 'translateX(0)';
        });

        setTimeout(() => {
            toast.style.transform = 'translateX(120%)';
            setTimeout(() => toast.remove(), 400);
        }, 3500);
    }

    // ===== Button Click Handlers with Toast =====
    const buttonActions = {
        // Hero buttons
        'btnExplore': () => {
            document.getElementById('courses').scrollIntoView({ behavior: 'smooth' });
            showToast('Explore our trending courses below!', 'compass', 'info');
        },
        'btnWatchDemo': () => showToast('Demo video loading... 🎬', 'play-circle', 'info'),
        'btnFreeConsult': () => showToast('Scheduling your free consultation!', 'headset', 'success'),
        'btnEnroll': () => {
            document.getElementById('courses').scrollIntoView({ behavior: 'smooth' });
            showToast('Choose a course to enroll!', 'graduation-cap', 'info');
        },

        // About buttons
        'btnLearnMission': () => showToast('Our mission: Empowering careers through tech!', 'bullseye', 'info'),
        'btnLearnVision': () => showToast('Vision: Global leader in EdTech! 🌍', 'eye', 'info'),
        'btnLearnValues': () => showToast('Innovation, Excellence, Integrity & Student-First!', 'heart', 'info'),
        'btnOurStory': () => showToast('Founded in 2013 by young entrepreneurs! 📖', 'book-open', 'info'),
        'btnMeetFounders': () => showToast('Meet our visionary founders! 👥', 'user-tie', 'info'),
        'btnAchievements': () => showToast('12+ years of excellence & 10K+ alumni! 🏆', 'trophy', 'success'),
        'btnPartners': () => showToast('Partnered with 500+ hiring companies! 🤝', 'handshake', 'success'),

        // Services buttons
        'btnTraining': () => showToast('Explore IT Training programs! 💻', 'laptop-code', 'info'),
        'btnPlacement': () => showToast('100% placement support guaranteed! 💼', 'briefcase', 'success'),
        'btnCertification': () => showToast('Industry-recognized certifications! 🏅', 'award', 'success'),
        'btnOnline': () => showToast('Learn online from anywhere! 🌐', 'globe', 'info'),
        'btnCorporate': () => showToast('Customized corporate training! 🏢', 'building', 'info'),
        'btnMentoring': () => showToast('Personal 1:1 mentoring sessions! 👨‍🏫', 'chalkboard-teacher', 'info'),
        'btnAllServices': () => showToast('Loading all 50+ services... ✨', 'th-large', 'info'),
        'btnCompare': () => showToast('Compare our training plans! ⚖️', 'balance-scale', 'info'),
        'btnCustomPlan': () => showToast('Create your custom learning plan! ✨', 'magic', 'warning'),

        // Stats buttons
        'btnViewReport': () => showToast('Annual report downloading... 📄', 'file-alt', 'info'),
        'btnSuccess': () => showToast('Read inspiring success stories! 📈', 'chart-line', 'success'),
        'btnTestimonials': () => showToast('See what students say about us! 💬', 'quote-right', 'info'),

        // Course enroll buttons
        'btnEnrollFullStack': () => showToast('Enrolling in Full Stack Development! 🚀', 'check-circle', 'success'),
        'btnEnrollAI': () => showToast('Enrolling in AI & Machine Learning! 🤖', 'check-circle', 'success'),
        'btnEnrollJava': () => showToast('Enrolling in Java Programming! ☕', 'check-circle', 'success'),
        'btnEnrollCloud': () => showToast('Enrolling in Cloud Computing! ☁️', 'check-circle', 'success'),
        'btnEnrollData': () => showToast('Enrolling in Data Science! 📊', 'check-circle', 'success'),
        'btnEnrollMobile': () => showToast('Enrolling in Mobile App Dev! 📱', 'check-circle', 'success'),
        'btnBrowseCourses': () => showToast('Loading 50+ courses catalog...', 'th', 'info'),
        'btnDownloadBrochure': () => showToast('Brochure downloading... 📥', 'download', 'success'),
        'btnScheduleDemo': () => showToast('Schedule a free demo class! 📅', 'calendar-alt', 'info'),

        // Team buttons
        'btnJoinTeam': () => showToast('Join our growing team! 🙌', 'user-plus', 'success'),
        'btnViewExperts': () => showToast('Meet our expert trainers! 👨‍🏫', 'chalkboard-teacher', 'info'),
        'btnCareers': () => showToast('Open positions available! 💼', 'suitcase', 'warning'),
        'btnInternship': () => showToast('Internship programs open! 🧪', 'flask', 'info'),

        // FAB items
        'fabChat': () => showToast('Live chat coming soon! 💬', 'comments', 'info'),
    };

    Object.entries(buttonActions).forEach(([id, handler]) => {
        const el = document.getElementById(id);
        if (el) {
            el.addEventListener('click', (e) => {
                e.preventDefault();
                handler();
            });
        }
    });

    // ===== Tilt Effect on Service Cards =====
    document.querySelectorAll('.service-card, .course-card').forEach(card => {
        card.addEventListener('mousemove', (e) => {
            const rect = card.getBoundingClientRect();
            const x = (e.clientX - rect.left) / rect.width;
            const y = (e.clientY - rect.top) / rect.height;
            const tiltX = (y - 0.5) * 8;
            const tiltY = (x - 0.5) * -8;
            card.style.transform = `perspective(600px) rotateX(${tiltX}deg) rotateY(${tiltY}deg) translateY(-4px)`;
        });

        card.addEventListener('mouseleave', () => {
            card.style.transform = 'perspective(600px) rotateX(0) rotateY(0) translateY(0)';
        });
    });

    // ===== Typewriter Effect for Hero Badge =====
    const badge = document.querySelector('.hero-badge span');
    if (badge) {
        const originalText = badge.textContent;
        badge.textContent = '';
        let charIndex = 0;

        function typeWriter() {
            if (charIndex < originalText.length) {
                badge.textContent += originalText.charAt(charIndex);
                charIndex++;
                setTimeout(typeWriter, 40);
            }
        }
        setTimeout(typeWriter, 1200);
    }

    // ===== Parallax on Hero Glows =====
    window.addEventListener('mousemove', (e) => {
        const x = e.clientX / window.innerWidth;
        const y = e.clientY / window.innerHeight;

        document.querySelectorAll('.hero-glow').forEach((glow, i) => {
            const speed = (i + 1) * 15;
            glow.style.transform = `translate(${x * speed}px, ${y * speed}px)`;
        });
    });

    console.log('%c🚀 Xplore IT Corp - About Page Loaded Successfully!', 'color: #6c5ce7; font-size: 16px; font-weight: bold;');
});
