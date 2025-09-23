// SAMA SYNDICAT - Documentation Website JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Initialize all components
    initSidebar();
    initSearch();
    initTabs();
    initAccordions();
    initTooltips();
    initProgressBars();
    initSmoothScroll();
    initPrintFunctionality();
    
    // Add fade-in animation to content
    const content = document.querySelector('.main-content');
    if (content) {
        content.classList.add('fade-in');
    }
});

// Sidebar functionality
function initSidebar() {
    const sidebarToggle = document.querySelector('.sidebar-toggle');
    const sidebar = document.querySelector('.sidebar');
    const sidebarLinks = document.querySelectorAll('.sidebar-link');
    
    // Toggle sidebar on mobile
    if (sidebarToggle && sidebar) {
        sidebarToggle.addEventListener('click', function() {
            sidebar.classList.toggle('show');
        });
        
        // Close sidebar when clicking outside on mobile
        document.addEventListener('click', function(e) {
            if (window.innerWidth <= 768 && 
                !sidebar.contains(e.target) && 
                !sidebarToggle.contains(e.target)) {
                sidebar.classList.remove('show');
            }
        });
    }
    
    // Handle sidebar submenu toggles
    sidebarLinks.forEach(link => {
        const hasSubmenu = link.nextElementSibling && 
                          link.nextElementSibling.classList.contains('sidebar-submenu');
        
        if (hasSubmenu) {
            link.addEventListener('click', function(e) {
                e.preventDefault();
                const submenu = this.nextElementSibling;
                submenu.classList.toggle('show');
                
                // Toggle arrow icon
                const arrow = this.querySelector('.arrow');
                if (arrow) {
                    arrow.classList.toggle('rotated');
                }
            });
        }
    });
    
    // Set active sidebar link based on current page
    const currentPath = window.location.pathname;
    sidebarLinks.forEach(link => {
        if (link.getAttribute('href') === currentPath || 
            link.getAttribute('href') === currentPath.split('/').pop()) {
            link.classList.add('active');
            
            // Open parent submenu if exists
            const parentSubmenu = link.closest('.sidebar-submenu');
            if (parentSubmenu) {
                parentSubmenu.classList.add('show');
                const parentLink = parentSubmenu.previousElementSibling;
                if (parentLink) {
                    const arrow = parentLink.querySelector('.arrow');
                    if (arrow) arrow.classList.add('rotated');
                }
            }
        }
    });
}

// Search functionality
function initSearch() {
    const searchInput = document.querySelector('.search-input');
    const searchableElements = document.querySelectorAll('[data-searchable]');
    
    if (searchInput && searchableElements.length > 0) {
        searchInput.addEventListener('input', function() {
            const query = this.value.toLowerCase().trim();
            
            searchableElements.forEach(element => {
                const text = element.textContent.toLowerCase();
                const isVisible = query === '' || text.includes(query);
                
                element.style.display = isVisible ? '' : 'none';
                
                // Highlight matching text
                if (query && isVisible) {
                    highlightText(element, query);
                } else {
                    removeHighlight(element);
                }
            });
            
            // Show "no results" message if needed
            const visibleElements = Array.from(searchableElements)
                .filter(el => el.style.display !== 'none');
            
            let noResultsMsg = document.querySelector('.no-results');
            if (visibleElements.length === 0 && query) {
                if (!noResultsMsg) {
                    noResultsMsg = document.createElement('div');
                    noResultsMsg.className = 'alert alert-info no-results';
                    noResultsMsg.innerHTML = '🔍 Aucun résultat trouvé pour votre recherche.';
                    searchInput.parentNode.insertAdjacentElement('afterend', noResultsMsg);
                }
            } else if (noResultsMsg) {
                noResultsMsg.remove();
            }
        });
    }
}

// Highlight search terms
function highlightText(element, query) {
    const walker = document.createTreeWalker(
        element,
        NodeFilter.SHOW_TEXT,
        null,
        false
    );
    
    const textNodes = [];
    let node;
    
    while (node = walker.nextNode()) {
        textNodes.push(node);
    }
    
    textNodes.forEach(textNode => {
        const text = textNode.textContent;
        const regex = new RegExp(`(${escapeRegExp(query)})`, 'gi');
        
        if (regex.test(text)) {
            const highlightedText = text.replace(regex, '<mark>$1</mark>');
            const span = document.createElement('span');
            span.innerHTML = highlightedText;
            textNode.parentNode.replaceChild(span, textNode);
        }
    });
}

// Remove highlights
function removeHighlight(element) {
    const marks = element.querySelectorAll('mark');
    marks.forEach(mark => {
        mark.outerHTML = mark.innerHTML;
    });
}

// Escape regex special characters
function escapeRegExp(string) {
    return string.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

// Tab functionality
function initTabs() {
    const tabButtons = document.querySelectorAll('.tab-button');
    const tabContents = document.querySelectorAll('.tab-content');
    
    tabButtons.forEach(button => {
        button.addEventListener('click', function() {
            const targetTab = this.getAttribute('data-tab');
            
            // Remove active class from all tabs and contents
            tabButtons.forEach(btn => btn.classList.remove('active'));
            tabContents.forEach(content => content.classList.remove('active'));
            
            // Add active class to clicked tab and corresponding content
            this.classList.add('active');
            const targetContent = document.querySelector(`[data-tab-content="${targetTab}"]`);
            if (targetContent) {
                targetContent.classList.add('active');
            }
        });
    });
}

// Accordion functionality
function initAccordions() {
    const accordionHeaders = document.querySelectorAll('.accordion-header');
    
    accordionHeaders.forEach(header => {
        header.addEventListener('click', function() {
            const content = this.nextElementSibling;
            const isOpen = content.classList.contains('show');
            
            // Close all accordions in the same group
            const group = this.closest('.accordion-group');
            if (group) {
                const allContents = group.querySelectorAll('.accordion-content');
                const allHeaders = group.querySelectorAll('.accordion-header');
                
                allContents.forEach(c => c.classList.remove('show'));
                allHeaders.forEach(h => h.classList.remove('active'));
            }
            
            // Toggle current accordion
            if (!isOpen) {
                content.classList.add('show');
                this.classList.add('active');
            }
        });
    });
}

// Tooltip functionality
function initTooltips() {
    const tooltipElements = document.querySelectorAll('[data-tooltip]');
    
    tooltipElements.forEach(element => {
        element.addEventListener('mouseenter', function() {
            const tooltipText = this.getAttribute('data-tooltip');
            const tooltip = document.createElement('div');
            tooltip.className = 'tooltip';
            tooltip.textContent = tooltipText;
            
            document.body.appendChild(tooltip);
            
            const rect = this.getBoundingClientRect();
            tooltip.style.left = rect.left + (rect.width / 2) - (tooltip.offsetWidth / 2) + 'px';
            tooltip.style.top = rect.top - tooltip.offsetHeight - 10 + 'px';
            
            this._tooltip = tooltip;
        });
        
        element.addEventListener('mouseleave', function() {
            if (this._tooltip) {
                this._tooltip.remove();
                this._tooltip = null;
            }
        });
    });
}

// Progress bar animation
function initProgressBars() {
    const progressBars = document.querySelectorAll('.progress-bar');
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const progressBar = entry.target;
                const targetWidth = progressBar.getAttribute('data-width') || '0%';
                
                setTimeout(() => {
                    progressBar.style.width = targetWidth;
                }, 200);
                
                observer.unobserve(progressBar);
            }
        });
    });
    
    progressBars.forEach(bar => observer.observe(bar));
}

// Smooth scroll for anchor links
function initSmoothScroll() {
    const anchorLinks = document.querySelectorAll('a[href^="#"]');
    
    anchorLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            const targetId = this.getAttribute('href').substring(1);
            const targetElement = document.getElementById(targetId);
            
            if (targetElement) {
                e.preventDefault();
                
                const headerHeight = document.querySelector('.header').offsetHeight;
                const targetPosition = targetElement.offsetTop - headerHeight - 20;
                
                window.scrollTo({
                    top: targetPosition,
                    behavior: 'smooth'
                });
            }
        });
    });
}

// Print functionality
function initPrintFunctionality() {
    const printButtons = document.querySelectorAll('.print-btn');
    
    printButtons.forEach(button => {
        button.addEventListener('click', function() {
            window.print();
        });
    });
}

// Utility functions
function showAlert(message, type = 'info') {
    const alert = document.createElement('div');
    alert.className = `alert alert-${type}`;
    alert.textContent = message;
    
    const container = document.querySelector('.main-content');
    container.insertBefore(alert, container.firstChild);
    
    setTimeout(() => {
        alert.remove();
    }, 5000);
}

function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        showAlert('Copié dans le presse-papiers !', 'success');
    }).catch(() => {
        showAlert('Erreur lors de la copie', 'danger');
    });
}

// Role-based content filtering
function filterByRole(role) {
    const roleElements = document.querySelectorAll('[data-role]');
    
    roleElements.forEach(element => {
        const elementRoles = element.getAttribute('data-role').split(',');
        const isVisible = role === 'all' || elementRoles.includes(role);
        
        element.style.display = isVisible ? '' : 'none';
    });
    
    // Update active filter button
    const filterButtons = document.querySelectorAll('.role-filter');
    filterButtons.forEach(button => {
        button.classList.toggle('active', button.getAttribute('data-role') === role);
    });
}

// Initialize role filters
document.addEventListener('DOMContentLoaded', function() {
    const roleFilters = document.querySelectorAll('.role-filter');
    
    roleFilters.forEach(filter => {
        filter.addEventListener('click', function() {
            const role = this.getAttribute('data-role');
            filterByRole(role);
        });
    });
});

// Training progress tracking
class TrainingProgress {
    constructor() {
        this.progress = JSON.parse(localStorage.getItem('trainingProgress') || '{}');
    }
    
    markComplete(moduleId) {
        this.progress[moduleId] = {
            completed: true,
            completedAt: new Date().toISOString()
        };
        this.save();
        this.updateUI();
    }
    
    isComplete(moduleId) {
        return this.progress[moduleId] && this.progress[moduleId].completed;
    }
    
    getCompletionRate() {
        const totalModules = document.querySelectorAll('[data-module-id]').length;
        const completedModules = Object.keys(this.progress).length;
        return totalModules > 0 ? (completedModules / totalModules) * 100 : 0;
    }
    
    save() {
        localStorage.setItem('trainingProgress', JSON.stringify(this.progress));
    }
    
    updateUI() {
        // Update completion checkmarks
        document.querySelectorAll('[data-module-id]').forEach(module => {
            const moduleId = module.getAttribute('data-module-id');
            const isCompleted = this.isComplete(moduleId);
            
            module.classList.toggle('completed', isCompleted);
            
            const checkmark = module.querySelector('.completion-checkmark');
            if (checkmark) {
                checkmark.style.display = isCompleted ? 'inline' : 'none';
            }
        });
        
        // Update overall progress bar
        const overallProgress = document.querySelector('.overall-progress');
        if (overallProgress) {
            const rate = this.getCompletionRate();
            overallProgress.style.width = rate + '%';
            
            const progressText = document.querySelector('.progress-text');
            if (progressText) {
                progressText.textContent = `${Math.round(rate)}% complété`;
            }
        }
    }
}

// Initialize training progress
const trainingProgress = new TrainingProgress();

document.addEventListener('DOMContentLoaded', function() {
    trainingProgress.updateUI();
    
    // Add completion buttons
    const completeButtons = document.querySelectorAll('.mark-complete');
    completeButtons.forEach(button => {
        button.addEventListener('click', function() {
            const moduleId = this.getAttribute('data-module-id');
            trainingProgress.markComplete(moduleId);
            showAlert('Module marqué comme terminé !', 'success');
        });
    });
});

// Export functions for global use
window.SamaSyndicatDocs = {
    showAlert,
    copyToClipboard,
    filterByRole,
    trainingProgress
};