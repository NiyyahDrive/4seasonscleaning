/* ================================================
   4 SEASONS - Main JavaScript
   Interactive functionality and UX enhancements
   ================================================ */

document.addEventListener('DOMContentLoaded', function() {
    setSeasonalTheme();
    initMobileMenu();
    initContactForm();
    initSmoothScroll();
    initScrollAnimations();
});

/* ================================================
   SEASONAL THEME
   ================================================ */

function setSeasonalTheme() {
    const month = new Date().getMonth();
    let season, seasonColor, seasonalMessage;
    
    if (month >= 2 && month <= 4) {
        season = 'lente';
        seasonColor = 'var(--season-spring)';
        seasonalMessage = 'Maak uw zonnepanelen klaar voor de zon. Vraag nu een voorjaarsreiniging aan.';
    } else if (month >= 5 && month <= 7) {
        season = 'zomer';
        seasonColor = 'var(--season-summer)';
        seasonalMessage = 'Schoon glas = koelere woning. Blijf fris en zuinig.';
    } else if (month >= 8 && month <= 10) {
        season = 'herfst';
        seasonColor = 'var(--season-autumn)';
        seasonalMessage = 'Bladvrije dakgoten = geen wateroverlast. Bescherm uw huis.';
    } else {
        season = 'winter';
        seasonColor = 'var(--season-winter)';
        seasonalMessage = 'Helder glas beschermt tegen kou en vocht. Winterkwaliteit.';
    }
    
    // Set data attribute on body
    document.body.setAttribute('data-season', season);
    
    // Update seasonal banner
    const banner = document.getElementById('seasonalBanner');
    const bannerText = document.getElementById('seasonalText');
    if (banner) {
        banner.setAttribute('data-season', season);
        if (bannerText) {
            bannerText.textContent = seasonalMessage;
        }
    }
    
    // Update CSS variable
    const seasonMap = {
        'lente': '#4ade80',
        'zomer': '#fbbf24',
        'herfst': '#f97316',
        'winter': '#0ea5e9'
    };
    document.documentElement.style.setProperty('--current-season', seasonMap[season]);
}

/* ================================================
   MOBILE MENU
   ================================================ */

function initMobileMenu() {
    const mobileMenuToggle = document.getElementById('mobileMenuToggle');
    const navMenu = document.getElementById('navMenu');

    if (!mobileMenuToggle) return;

    mobileMenuToggle.addEventListener('click', function() {
        navMenu.classList.toggle('active');
    });

    // Close menu when a link is clicked
    const navLinks = navMenu.querySelectorAll('.nav-link');
    navLinks.forEach(link => {
        link.addEventListener('click', function() {
            navMenu.classList.remove('active');
        });
    });

    // Close menu when clicking outside
    document.addEventListener('click', function(event) {
        if (!event.target.closest('.navbar')) {
            navMenu.classList.remove('active');
        }
    });
}

/* ================================================
   CONTACT FORM HANDLING
   ================================================ */

function initContactForm() {
    const form = document.getElementById('contactForm');
    
    if (!form) return;

    form.addEventListener('submit', async function(e) {
        e.preventDefault();

        // Get form data
        const formData = new FormData(form);
        const data = {
            name: formData.get('name'),
            email: formData.get('email'),
            phone: formData.get('phone'),
            service: formData.get('service'),
            message: formData.get('message'),
            timestamp: new Date().toISOString()
        };

        // Basic validation
        if (!data.name || !data.email || !data.service || !data.message) {
            showNotification('Vul alstublieft alle verplichte velden in', 'error');
            return;
        }

        // Email validation
        if (!isValidEmail(data.email)) {
            showNotification('Voer alstublieft een geldig e-mailadres in', 'error');
            return;
        }

        // Show loading state
        const submitBtn = form.querySelector('button[type="submit"]');
        const originalText = submitBtn.textContent;
        submitBtn.textContent = 'Verzenden...';
        submitBtn.disabled = true;

        // Simulate form submission (in production, send to backend)
        try {
            await new Promise(resolve => setTimeout(resolve, 1500));

            // Log data (in production, send to API)
            console.log('Form submitted:', data);

            // Show success message
            showNotification('Bedankt! We nemen snel contact met je op.', 'success');

            // Reset form
            form.reset();

            // Restore button
            submitBtn.textContent = originalText;
            submitBtn.disabled = false;

        } catch (error) {
            console.error('Error:', error);
            showNotification('Er is iets misgegaan. Probeer later opnieuw.', 'error');
            submitBtn.textContent = originalText;
            submitBtn.disabled = false;
        }
    });
}

/* ================================================
   FORM UTILITIES
   ================================================ */

function isValidEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background-color: ${type === 'success' ? '#2d5c3d' : type === 'error' ? '#dc2626' : '#1e3a5f'};
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 0.375rem;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
        z-index: 1000;
        animation: slideIn 0.3s ease;
        font-weight: 500;
    `;

    document.body.appendChild(notification);

    // Remove notification after 5 seconds
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease';
        setTimeout(() => notification.remove(), 300);
    }, 5000);
}

/* ================================================
   SMOOTH SCROLL
   ================================================ */

function initSmoothScroll() {
    const links = document.querySelectorAll('a[href^="#"]');
    
    links.forEach(link => {
        link.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            
            if (href === '#') {
                e.preventDefault();
                return;
            }

            const target = document.querySelector(href);
            
            if (target) {
                e.preventDefault();
                target.scrollIntoView({ behavior: 'smooth' });
            }
        });
    });
}

/* ================================================
   SCROLL ANIMATIONS
   ================================================ */

function initScrollAnimations() {
    const elements = document.querySelectorAll('.service-card, .trust-item, .value-card, .team-member');
    
    if (!elements.length) return;

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.animation = 'fadeInUp 0.6s ease forwards';
                observer.unobserve(entry.target);
            }
        });
    }, {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    });

    elements.forEach(el => observer.observe(el));
}

/* ================================================
   ANIMATIONS (CSS)
   ================================================ */

// Add animation styles dynamically
function addAnimationStyles() {
    const style = document.createElement('style');
    style.textContent = `
        @keyframes slideIn {
            from {
                transform: translateX(100%);
                opacity: 0;
            }
            to {
                transform: translateX(0);
                opacity: 1;
            }
        }

        @keyframes slideOut {
            from {
                transform: translateX(0);
                opacity: 1;
            }
            to {
                transform: translateX(100%);
                opacity: 0;
            }
        }

        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translateY(20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        @keyframes fadeIn {
            from {
                opacity: 0;
            }
            to {
                opacity: 1;
            }
        }
    `;
    document.head.appendChild(style);
}

// Call animation styles on page load
addAnimationStyles();

/* ================================================
   UTILITY: Get URL Parameters
   ================================================ */

function getUrlParameter(name) {
    const params = new URLSearchParams(window.location.search);
    return params.get(name);
}

// Example: Auto-select service if passed in URL
document.addEventListener('DOMContentLoaded', function() {
    const serviceParam = getUrlParameter('type');
    const serviceSelect = document.getElementById('service');
    
    if (serviceParam && serviceSelect) {
        serviceSelect.value = serviceParam;
    }
});

/* ================================================
   LAZY LOADING IMAGES (Optional)
   ================================================ */

function initLazyLoading() {
    if ('IntersectionObserver' in window) {
        const images = document.querySelectorAll('img[data-src]');
        
        const imageObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src;
                    img.removeAttribute('data-src');
                    imageObserver.unobserve(img);
                }
            });
        });
        
        images.forEach(img => imageObserver.observe(img));
    }
}

// Initialize on load if needed
// initLazyLoading();

/* ================================================
   ANALYTICS TRACKING (Optional - Google Analytics pattern)
   ================================================ */

function trackEvent(category, action, label) {
    if (typeof gtag !== 'undefined') {
        gtag('event', action, {
            'event_category': category,
            'event_label': label
        });
    }
}

// Example: Track CTA clicks
document.querySelectorAll('.btn-primary').forEach(btn => {
    btn.addEventListener('click', function() {
        trackEvent('engagement', 'cta_click', this.textContent);
    });
});

/* ================================================
   DARK MODE TOGGLE (Optional)
   ================================================ */

function initDarkMode() {
    const darkModeToggle = document.getElementById('darkModeToggle');
    
    if (!darkModeToggle) return;

    const isDarkMode = localStorage.getItem('darkMode') === 'true';
    
    if (isDarkMode) {
        document.body.classList.add('dark-mode');
        darkModeToggle.checked = true;
    }

    darkModeToggle.addEventListener('change', function() {
        if (this.checked) {
            document.body.classList.add('dark-mode');
            localStorage.setItem('darkMode', 'true');
        } else {
            document.body.classList.remove('dark-mode');
            localStorage.setItem('darkMode', 'false');
        }
    });
}

/* ================================================
   PERFORMANCE: Prefetch DNS
   ================================================ */

function prefetchDns() {
    const link = document.createElement('link');
    link.rel = 'dns-prefetch';
    link.href = '//fonts.googleapis.com';
    document.head.appendChild(link);
}

prefetchDns();

/* ================================================
   UTILITY: Debounce Function
   ================================================ */

function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

/* ================================================
   CONSOLE LOG (Development info)
   ================================================ */

console.log('%c4 SEASONS', 'font-size: 20px; font-weight: bold; color: #1e3a5f;');
console.log('%cProfessionele reiniging en onderhoud in Vlaanderen', 'font-size: 12px; color: #666;');
console.log('%cInfo: https://www.4seasonscleaning.be', 'font-size: 12px; color: #666;');
