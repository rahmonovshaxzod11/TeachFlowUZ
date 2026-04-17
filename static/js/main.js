/**
 * TeachFlowUZ — Main JavaScript
 * Global: sidebar navigation, mobile menu, animations, drag & drop
 */

document.addEventListener('DOMContentLoaded', () => {
    initMobileMenu();
    initScrollAnimations();
    initActiveNav();
});

/* ── Mobile Menu ────────────────────────────────────────────── */
function initMobileMenu() {
    const menuBtn = document.getElementById('mobile-menu-btn');
    const sidebar = document.getElementById('sidebar');
    const overlay = document.getElementById('sidebar-overlay');

    if (menuBtn && sidebar) {
        menuBtn.addEventListener('click', () => {
            sidebar.classList.toggle('open');
            if (overlay) overlay.classList.toggle('visible');
        });

        if (overlay) {
            overlay.addEventListener('click', () => {
                sidebar.classList.remove('open');
                overlay.classList.remove('visible');
            });
        }
    }
}

/* ── Scroll Animations ──────────────────────────────────────── */
function initScrollAnimations() {
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-fade-in-up');
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.1 });

    document.querySelectorAll('.animate-on-scroll').forEach(el => {
        observer.observe(el);
    });
}

/* ── Active Navigation ──────────────────────────────────────── */
function initActiveNav() {
    const currentPath = window.location.pathname;
    document.querySelectorAll('.nav-item').forEach(item => {
        if (item.getAttribute('href') === currentPath) {
            item.classList.add('active');
        }
    });
}

/* ── Drag & Drop File Upload ─────────────────────────────────── */
function initFileUpload(zoneId, fileInfoId, inputId) {
    const zone = document.getElementById(zoneId);
    const fileInfo = document.getElementById(fileInfoId);
    const input = document.getElementById(inputId);

    if (!zone || !input) return;

    // Prevent defaults
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        zone.addEventListener(eventName, e => {
            e.preventDefault();
            e.stopPropagation();
        });
    });

    // Highlight on drag
    ['dragenter', 'dragover'].forEach(eventName => {
        zone.addEventListener(eventName, () => zone.classList.add('dragover'));
    });

    ['dragleave', 'drop'].forEach(eventName => {
        zone.addEventListener(eventName, () => zone.classList.remove('dragover'));
    });

    // Handle drop
    zone.addEventListener('drop', e => {
        const files = e.dataTransfer.files;
        if (files.length) {
            input.files = files;
            showFileInfo(files[0], fileInfo);
        }
    });

    // Handle file select
    input.addEventListener('change', () => {
        if (input.files.length) {
            showFileInfo(input.files[0], fileInfo);
        }
    });
}

function showFileInfo(file, fileInfoEl) {
    if (!fileInfoEl) return;

    const ext = file.name.split('.').pop().toLowerCase();
    const icons = {
        'pdf': '📄',
        'docx': '📝',
        'doc': '📝',
        'pptx': '📊',
        'ppt': '📊',
        'mp4': '🎬',
        'avi': '🎬',
        'mov': '🎬',
    };

    const icon = icons[ext] || '📁';
    const size = formatFileSize(file.size);

    fileInfoEl.innerHTML = `
        <span class="upload-file-icon">${icon}</span>
        <div>
            <div class="upload-file-name">${file.name}</div>
            <div class="upload-file-size">${size}</div>
        </div>
        <button type="button" class="upload-file-remove" onclick="removeFile(this)" title="Olib tashlash">✕</button>
    `;
    fileInfoEl.classList.add('visible');
}

function removeFile(btn) {
    const fileInfo = btn.closest('.upload-file-info');
    const form = btn.closest('form');
    if (form) {
        const input = form.querySelector('input[type="file"]');
        if (input) input.value = '';
    }
    if (fileInfo) fileInfo.classList.remove('visible');
}

function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

/* ── Processing Overlay ──────────────────────────────────────── */
function showProcessing() {
    const overlay = document.getElementById('processing-overlay');
    if (overlay) {
        overlay.classList.add('visible');
        animateProcessingSteps();
    }
}

function hideProcessing() {
    const overlay = document.getElementById('processing-overlay');
    if (overlay) overlay.classList.remove('visible');
}

function animateProcessingSteps() {
    const steps = document.querySelectorAll('.processing-step');
    let current = 0;

    function advanceStep() {
        if (current < steps.length) {
            if (current > 0) {
                steps[current - 1].classList.remove('active');
                steps[current - 1].classList.add('done');
                steps[current - 1].querySelector('.processing-step-icon').textContent = '✓';
            }
            steps[current].classList.add('active');
            current++;

            if (current < steps.length) {
                setTimeout(advanceStep, 2000 + Math.random() * 3000);
            }
        }
    }

    advanceStep();
}

/* ── Modal ────────────────────────────────────────────────────── */
function openModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) modal.classList.add('visible');
}

function closeModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) modal.classList.remove('visible');
}

/* ── Toast Notifications ─────────────────────────────────────── */
function showToast(message, type = 'info') {
    const toast = document.createElement('div');
    toast.className = `alert alert-${type}`;
    toast.style.cssText = 'position:fixed;top:20px;right:20px;z-index:999;max-width:400px;animation:fadeInDown 0.3s ease;';
    toast.textContent = message;

    document.body.appendChild(toast);

    setTimeout(() => {
        toast.style.animation = 'fadeIn 0.3s ease reverse';
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

/* ── Tabs ─────────────────────────────────────────────────────── */
function switchTab(tabName, containerId) {
    const container = containerId ? document.getElementById(containerId) : document;

    // Update tab buttons
    container.querySelectorAll('.tab').forEach(tab => {
        tab.classList.toggle('active', tab.dataset.tab === tabName);
    });

    // Update tab content
    container.querySelectorAll('.tab-content').forEach(content => {
        content.classList.toggle('active', content.id === `tab-${tabName}`);
    });
}
