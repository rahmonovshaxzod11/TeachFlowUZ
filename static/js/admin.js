/**
 * TeachFlowUZ — Admin Panel JavaScript
 * CRUD operations with AJAX
 */

/* ── Admin Tabs ──────────────────────────────────────────────── */
function switchAdminTab(tabName) {
    document.querySelectorAll('.admin-tab-btn').forEach(btn => {
        btn.classList.toggle('active', btn.dataset.tab === tabName);
    });

    document.querySelectorAll('.admin-tab-content').forEach(content => {
        content.classList.toggle('active', content.id === `admin-tab-${tabName}`);
    });
}

/* ── Module CRUD ─────────────────────────────────────────────── */
function openModuleModal(moduleData = null) {
    const modal = document.getElementById('module-modal');
    const form = document.getElementById('module-form');
    const title = document.getElementById('module-modal-title');

    if (moduleData) {
        title.textContent = 'Modulni Tahrirlash';
        form.dataset.id = moduleData.id;
        form.querySelector('[name="title"]').value = moduleData.title;
        form.querySelector('[name="description"]').value = moduleData.description || '';
        form.querySelector('[name="icon"]').value = moduleData.icon || '📚';
    } else {
        title.textContent = 'Yangi Modul';
        form.dataset.id = '';
        form.reset();
    }

    openModal('module-modal');
}

async function saveModule(event) {
    event.preventDefault();
    const form = event.target;
    const id = form.dataset.id;
    const data = {
        title: form.querySelector('[name="title"]').value,
        description: form.querySelector('[name="description"]').value,
        icon: form.querySelector('[name="icon"]').value || '📚',
    };

    try {
        const url = id ? `/api/admin/modules/${id}` : '/api/admin/modules';
        const method = id ? 'PUT' : 'POST';

        const resp = await fetch(url, {
            method,
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data),
        });

        if (resp.ok) {
            showToast(id ? 'Modul yangilandi!' : 'Yangi modul yaratildi!', 'success');
            closeModal('module-modal');
            setTimeout(() => location.reload(), 500);
        } else {
            const err = await resp.json();
            showToast(err.error || 'Xatolik yuz berdi', 'danger');
        }
    } catch (err) {
        showToast('Server bilan bog\'lanib bo\'lmadi', 'danger');
    }
}

async function deleteModule(id) {
    if (!confirm('Modulni o\'chirishni xohlaysizmi? Barcha darslar, testlar va topshiriqlar ham o\'chiriladi!')) return;

    try {
        const resp = await fetch(`/api/admin/modules/${id}`, { method: 'DELETE' });
        if (resp.ok) {
            showToast('Modul o\'chirildi', 'success');
            setTimeout(() => location.reload(), 500);
        } else {
            showToast('Xatolik yuz berdi', 'danger');
        }
    } catch (err) {
        showToast('Server bilan bog\'lanib bo\'lmadi', 'danger');
    }
}

/* ── Lesson CRUD ─────────────────────────────────────────────── */
function openLessonModal(lessonData = null) {
    const modal = document.getElementById('lesson-modal');
    const form = document.getElementById('lesson-form');
    const title = document.getElementById('lesson-modal-title');

    if (lessonData) {
        title.textContent = 'Darsni Tahrirlash';
        form.dataset.id = lessonData.id;
        form.querySelector('[name="title"]').value = lessonData.title;
        form.querySelector('[name="description"]').value = lessonData.description || '';
        form.querySelector('[name="video_url"]').value = lessonData.video_url || '';
        form.querySelector('[name="duration"]').value = lessonData.duration || '';
        form.querySelector('[name="module_id"]').value = lessonData.module_id;
    } else {
        title.textContent = 'Yangi Dars';
        form.dataset.id = '';
        form.reset();
    }

    openModal('lesson-modal');
}

async function saveLesson(event) {
    event.preventDefault();
    const form = event.target;
    const id = form.dataset.id;
    const data = {
        title: form.querySelector('[name="title"]').value,
        description: form.querySelector('[name="description"]').value,
        video_url: form.querySelector('[name="video_url"]').value,
        duration: form.querySelector('[name="duration"]').value,
        module_id: parseInt(form.querySelector('[name="module_id"]').value),
    };

    try {
        const url = id ? `/api/admin/lessons/${id}` : '/api/admin/lessons';
        const method = id ? 'PUT' : 'POST';

        const resp = await fetch(url, {
            method,
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data),
        });

        if (resp.ok) {
            showToast(id ? 'Dars yangilandi!' : 'Yangi dars yaratildi!', 'success');
            closeModal('lesson-modal');
            setTimeout(() => location.reload(), 500);
        } else {
            const err = await resp.json();
            showToast(err.error || 'Xatolik yuz berdi', 'danger');
        }
    } catch (err) {
        showToast('Server bilan bog\'lanib bo\'lmadi', 'danger');
    }
}

async function deleteLesson(id) {
    if (!confirm('Darsni o\'chirishni xohlaysizmi?')) return;

    try {
        const resp = await fetch(`/api/admin/lessons/${id}`, { method: 'DELETE' });
        if (resp.ok) {
            showToast('Dars o\'chirildi', 'success');
            setTimeout(() => location.reload(), 500);
        } else {
            showToast('Xatolik yuz berdi', 'danger');
        }
    } catch (err) {
        showToast('Server bilan bog\'lanib bo\'lmadi', 'danger');
    }
}

/* ── Test CRUD ───────────────────────────────────────────────── */
function openTestModal(testData = null) {
    const modal = document.getElementById('test-modal');
    const form = document.getElementById('test-form');
    const title = document.getElementById('test-modal-title');

    if (testData) {
        title.textContent = 'Testni Tahrirlash';
        form.dataset.id = testData.id;
        form.querySelector('[name="question"]').value = testData.question;
        form.querySelector('[name="option_a"]').value = testData.option_a;
        form.querySelector('[name="option_b"]').value = testData.option_b;
        form.querySelector('[name="option_c"]').value = testData.option_c;
        form.querySelector('[name="option_d"]').value = testData.option_d;
        form.querySelector('[name="correct_answer"]').value = testData.correct_answer;
        form.querySelector('[name="explanation"]').value = testData.explanation || '';
        form.querySelector('[name="module_id"]').value = testData.module_id;
    } else {
        title.textContent = 'Yangi Test Savoli';
        form.dataset.id = '';
        form.reset();
    }

    openModal('test-modal');
}

async function saveTest(event) {
    event.preventDefault();
    const form = event.target;
    const id = form.dataset.id;
    const data = {
        question: form.querySelector('[name="question"]').value,
        option_a: form.querySelector('[name="option_a"]').value,
        option_b: form.querySelector('[name="option_b"]').value,
        option_c: form.querySelector('[name="option_c"]').value,
        option_d: form.querySelector('[name="option_d"]').value,
        correct_answer: form.querySelector('[name="correct_answer"]').value,
        explanation: form.querySelector('[name="explanation"]').value,
        module_id: parseInt(form.querySelector('[name="module_id"]').value),
    };

    try {
        const url = id ? `/api/admin/tests/${id}` : '/api/admin/tests';
        const method = id ? 'PUT' : 'POST';

        const resp = await fetch(url, {
            method,
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data),
        });

        if (resp.ok) {
            showToast(id ? 'Test yangilandi!' : 'Yangi test yaratildi!', 'success');
            closeModal('test-modal');
            setTimeout(() => location.reload(), 500);
        } else {
            const err = await resp.json();
            showToast(err.error || 'Xatolik yuz berdi', 'danger');
        }
    } catch (err) {
        showToast('Server bilan bog\'lanib bo\'lmadi', 'danger');
    }
}

async function deleteTest(id) {
    if (!confirm('Test savolini o\'chirishni xohlaysizmi?')) return;

    try {
        const resp = await fetch(`/api/admin/tests/${id}`, { method: 'DELETE' });
        if (resp.ok) {
            showToast('Test o\'chirildi', 'success');
            setTimeout(() => location.reload(), 500);
        } else {
            showToast('Xatolik yuz berdi', 'danger');
        }
    } catch (err) {
        showToast('Server bilan bog\'lanib bo\'lmadi', 'danger');
    }
}

/* ── Assignment CRUD ─────────────────────────────────────────── */
function openAssignmentModal(assignmentData = null) {
    const modal = document.getElementById('assignment-modal');
    const form = document.getElementById('assignment-form');
    const title = document.getElementById('assignment-modal-title');

    if (assignmentData) {
        title.textContent = 'Topshiriqni Tahrirlash';
        form.dataset.id = assignmentData.id;
        form.querySelector('[name="title"]').value = assignmentData.title;
        form.querySelector('[name="description"]').value = assignmentData.description || '';
        form.querySelector('[name="assignment_type"]').value = assignmentData.assignment_type || 'document';
        form.querySelector('[name="accepted_formats"]').value = assignmentData.accepted_formats || 'pdf,docx,pptx';
        form.querySelector('[name="module_id"]').value = assignmentData.module_id;
    } else {
        title.textContent = 'Yangi Topshiriq';
        form.dataset.id = '';
        form.reset();
    }

    openModal('assignment-modal');
}

async function saveAssignment(event) {
    event.preventDefault();
    const form = event.target;
    const id = form.dataset.id;
    const data = {
        title: form.querySelector('[name="title"]').value,
        description: form.querySelector('[name="description"]').value,
        assignment_type: form.querySelector('[name="assignment_type"]').value,
        accepted_formats: form.querySelector('[name="accepted_formats"]').value,
        module_id: parseInt(form.querySelector('[name="module_id"]').value),
    };

    try {
        const url = id ? `/api/admin/assignments/${id}` : '/api/admin/assignments';
        const method = id ? 'PUT' : 'POST';

        const resp = await fetch(url, {
            method,
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data),
        });

        if (resp.ok) {
            showToast(id ? 'Topshiriq yangilandi!' : 'Yangi topshiriq yaratildi!', 'success');
            closeModal('assignment-modal');
            setTimeout(() => location.reload(), 500);
        } else {
            const err = await resp.json();
            showToast(err.error || 'Xatolik yuz berdi', 'danger');
        }
    } catch (err) {
        showToast('Server bilan bog\'lanib bo\'lmadi', 'danger');
    }
}

async function deleteAssignment(id) {
    if (!confirm('Topshiriqni o\'chirishni xohlaysizmi?')) return;

    try {
        const resp = await fetch(`/api/admin/assignments/${id}`, { method: 'DELETE' });
        if (resp.ok) {
            showToast('Topshiriq o\'chirildi', 'success');
            setTimeout(() => location.reload(), 500);
        } else {
            showToast('Xatolik yuz berdi', 'danger');
        }
    } catch (err) {
        showToast('Server bilan bog\'lanib bo\'lmadi', 'danger');
    }
}
