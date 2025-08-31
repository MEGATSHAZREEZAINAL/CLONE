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

    // Mobile navigation toggle
    const mobileNavToggle = document.querySelector('.mobile-nav-toggle');
    const navLinks = document.querySelector('.nav-links');
    
    if (mobileNavToggle) {
        mobileNavToggle.addEventListener('click', () => {
            navLinks.classList.toggle('active');
            document.body.classList.toggle('nav-open');
            
            // Change hamburger icon to close icon and vice versa
            const isOpen = navLinks.classList.contains('active');
            mobileNavToggle.innerHTML = isOpen ? '<i class="fas fa-times"></i>' : '<i class="fas fa-bars"></i>';
        });
        
        // Close mobile menu when clicking outside
        document.addEventListener('click', (e) => {
            if (navLinks.classList.contains('active') && 
                !navLinks.contains(e.target) && 
                !mobileNavToggle.contains(e.target)) {
                navLinks.classList.remove('active');
                document.body.classList.remove('nav-open');
                mobileNavToggle.innerHTML = '<i class="fas fa-bars"></i>';
            }
        });
    }

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

    // Form validation and submission
    const forms = document.querySelectorAll('form');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            
            // Check if it's a newsletter form
            if (form.closest('.footer-newsletter')) {
                const emailInput = form.querySelector('input[type="email"]');
                const email = emailInput.value.trim();
                
                if (email && isValidEmail(email)) {
                    // Simulate form submission
                    emailInput.value = '';
                    showToast('Success', 'Thanks for subscribing to our newsletter!', 'success');
                } else {
                    showToast('Error', 'Please enter a valid email address.', 'error');
                }
                return;
            }
            
            // For other forms, validate all required fields
            const requiredFields = form.querySelectorAll('[required]');
            let isValid = true;
            
            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    isValid = false;
                    showFieldError(field, 'This field is required');
                } else if (field.type === 'email' && !isValidEmail(field.value.trim())) {
                    isValid = false;
                    showFieldError(field, 'Please enter a valid email address');
                } else {
                    clearFieldError(field);
                }
            });
            
            if (isValid) {
                // Simulate form submission
                showToast('Success', 'Form submitted successfully!', 'success');
                form.reset();
            }
        });
    });
    
    // Show field error message
    function showFieldError(field, message) {
        // Clear any existing error
        clearFieldError(field);
        
        // Add error class to the field
        field.classList.add('is-invalid');
        
        // Create and append error message
        const errorDiv = document.createElement('div');
        errorDiv.className = 'form-error';
        errorDiv.textContent = message;
        
        const formGroup = field.closest('.form-group');
        if (formGroup) {
            formGroup.appendChild(errorDiv);
        } else {
            field.parentNode.insertBefore(errorDiv, field.nextSibling);
        }
    }
    
    // Clear field error message
    function clearFieldError(field) {
        field.classList.remove('is-invalid');
        
        const formGroup = field.closest('.form-group');
        if (formGroup) {
            const errorDiv = formGroup.querySelector('.form-error');
            if (errorDiv) {
                errorDiv.remove();
            }
        }
    }

    // Email validation helper
    function isValidEmail(email) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    }

    // Toast notification system
    function showToast(title, message, type = 'info') {
        // Create toast container if it doesn't exist
        let toastContainer = document.querySelector('.toast-container');
        if (!toastContainer) {
            toastContainer = document.createElement('div');
            toastContainer.className = 'toast-container';
            document.body.appendChild(toastContainer);
        }
        
        // Create toast element
        const toast = document.createElement('div');
        toast.className = `toast ${type}`;
        
        // Set toast content
        toast.innerHTML = `
            <div class="toast-icon">
                <i class="fas ${getIconForToastType(type)}"></i>
            </div>
            <div class="toast-content">
                <div class="toast-title">${title}</div>
                <div class="toast-message">${message}</div>
            </div>
            <button class="toast-close">
                <i class="fas fa-times"></i>
            </button>
        `;
        
        // Add toast to container
        toastContainer.appendChild(toast);
        
        // Add close functionality
        const closeBtn = toast.querySelector('.toast-close');
        closeBtn.addEventListener('click', () => {
            toast.style.animation = 'slideOut 0.3s forwards';
            setTimeout(() => {
                toast.remove();
            }, 300);
        });
        
        // Auto remove after 5 seconds
        setTimeout(() => {
            if (toast.parentNode) {
                toast.style.animation = 'slideOut 0.3s forwards';
                setTimeout(() => {
                    if (toast.parentNode) {
                        toast.remove();
                    }
                }, 300);
            }
        }, 5000);
    }
    
    // Get appropriate icon for toast type
    function getIconForToastType(type) {
        switch (type) {
            case 'success': return 'fa-check-circle';
            case 'error': return 'fa-exclamation-circle';
            case 'warning': return 'fa-exclamation-triangle';
            case 'info': 
            default: return 'fa-info-circle';
        }
    }

    // Modal functionality
    const modalTriggers = document.querySelectorAll('[data-modal]');
    
    modalTriggers.forEach(trigger => {
        trigger.addEventListener('click', (e) => {
            e.preventDefault();
            
            const modalId = trigger.getAttribute('data-modal');
            const modal = document.getElementById(modalId);
            
            if (modal) {
                openModal(modal);
            }
        });
    });
    
    // Open modal function
    function openModal(modal) {
        const overlay = modal.closest('.modal-overlay');
        if (overlay) {
            overlay.classList.add('active');
            document.body.style.overflow = 'hidden';
            
            // Close modal when clicking on overlay
            overlay.addEventListener('click', (e) => {
                if (e.target === overlay) {
                    closeModal(modal);
                }
            });
            
            // Close modal when clicking close button
            const closeBtn = modal.querySelector('.modal-close');
            if (closeBtn) {
                closeBtn.addEventListener('click', () => {
                    closeModal(modal);
                });
            }
            
            // Close modal with Escape key
            document.addEventListener('keydown', (e) => {
                if (e.key === 'Escape' && overlay.classList.contains('active')) {
                    closeModal(modal);
                }
            });
        }
    }
    
    // Close modal function
    function closeModal(modal) {
        const overlay = modal.closest('.modal-overlay');
        if (overlay) {
            overlay.classList.remove('active');
            document.body.style.overflow = '';
        }
    }

    // Auth tabs functionality
    const authTabs = document.querySelectorAll('.auth-tab');
    const authForms = document.querySelectorAll('.auth-form');
    
    authTabs.forEach(tab => {
        tab.addEventListener('click', () => {
            // Remove active class from all tabs and forms
            authTabs.forEach(t => t.classList.remove('active'));
            authForms.forEach(f => f.classList.remove('active'));
            
            // Add active class to clicked tab
            tab.classList.add('active');
            
            // Show corresponding form
            const formId = tab.getAttribute('data-form');
            document.getElementById(formId).classList.add('active');
        });
    });

    // Intersection Observer for animations
    const animatedElements = document.querySelectorAll('.hero, .features, .integrations, .solutions, .testimonials, .pricing-card, .auth-container');
    
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

