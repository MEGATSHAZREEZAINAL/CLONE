document.addEventListener('DOMContentLoaded', function() {
    // Role tabs functionality
    const roleTabs = document.querySelectorAll('.role-tab');
    const roleContents = document.querySelectorAll('.role-content');

    roleTabs.forEach(tab => {
        tab.addEventListener('click', () => {
            // Remove active class from all tabs and contents
            roleTabs.forEach(t => t.classList.remove('active'));
            roleContents.forEach(c => c.classList.remove('active'));
            
            // Add active class to clicked tab
            tab.classList.add('active');
            
            // Show corresponding content
            const role = tab.getAttribute('data-role');
            document.getElementById(`${role}-content`).classList.add('active');
        });
    });

    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            
            const targetId = this.getAttribute('href');
            if (targetId === '#') return;
            
            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                window.scrollTo({
                    top: targetElement.offsetTop - 100,
                    behavior: 'smooth'
                });
            }
        });
    });

    // Mobile navigation toggle (to be implemented with a hamburger menu)
    // This is a placeholder for future implementation
    const mobileNavToggle = () => {
        // Code for mobile navigation toggle
        console.log('Mobile navigation toggle functionality to be implemented');
    };

    // Testimonial carousel (simple version)
    let currentTestimonialIndex = 0;
    const testimonials = document.querySelectorAll('.testimonial-card');
    const totalTestimonials = testimonials.length;

    // Auto-rotate testimonials every 5 seconds
    if (totalTestimonials > 4) { // Only activate if there are more than 4 testimonials
        setInterval(() => {
            testimonials.forEach(testimonial => {
                testimonial.style.display = 'none';
            });

            // Show next 4 testimonials
            for (let i = 0; i < 4; i++) {
                const index = (currentTestimonialIndex + i) % totalTestimonials;
                if (testimonials[index]) {
                    testimonials[index].style.display = 'block';
                }
            }

            currentTestimonialIndex = (currentTestimonialIndex + 1) % totalTestimonials;
        }, 5000);
    }

    // Form submission handling
    const newsletterForm = document.querySelector('.footer-newsletter form');
    if (newsletterForm) {
        newsletterForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const emailInput = this.querySelector('input[type="email"]');
            const email = emailInput.value.trim();
            
            if (email && isValidEmail(email)) {
                // Simulate form submission
                console.log('Newsletter subscription for:', email);
                emailInput.value = '';
                alert('Thanks for subscribing to our newsletter!');
            } else {
                alert('Please enter a valid email address.');
            }
        });
    }

    // Email validation helper
    function isValidEmail(email) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    }

    // Intersection Observer for animations
    const animatedElements = document.querySelectorAll('.hero, .features, .integrations, .solutions, .testimonials');
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = 1;
                entry.target.style.transform = 'translateY(0)';
                observer.unobserve(entry.target);
            }
        });
    }, {
        threshold: 0.1
    });
    
    animatedElements.forEach(element => {
        element.style.opacity = 0;
        element.style.transform = 'translateY(20px)';
        element.style.transition = 'opacity 0.8s ease-out, transform 0.8s ease-out';
        observer.observe(element);
    });
});

