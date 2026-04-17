"""
TeachFlowUZ — Main Flask Application
Pedagogika bo'yicha ta'lim platformasi
"""

import os
import json
import threading
from datetime import datetime

from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
from werkzeug.utils import secure_filename
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from functools import wraps

from models import db, Module, Lesson, Test, Assignment, Submission, User
from seed_data import seed_database
from ai_service import evaluate_submission

# ── App Configuration ────────────────────────────────────────────
app = Flask(__name__)
app.secret_key = 'teachflowuz-secret-key-2024'

# Database
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir, "teachflow.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# File uploads
UPLOAD_FOLDER = os.path.join(basedir, 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB

ALLOWED_EXTENSIONS = {'pdf', 'docx', 'doc', 'pptx', 'ppt', 'mp4', 'avi', 'mov', 'mkv'}

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = "Iltimos, avval tizimga kiring."
login_manager.login_message_category = "info"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin():
            flash('Sizda ushbu sahifaga kirish huquqi yo\'q!', 'danger')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# ── Context Processor ────────────────────────────────────────────
@app.context_processor
def inject_globals():
    """Barcha templatelar uchun umumiy ma'lumotlar"""
    modules_nav = Module.query.order_by(Module.order).all()
    module_count = Module.query.count()
    return {
        'modules_nav': modules_nav,
        'module_count': module_count,
    }


# ═══════════════════════════════════════════════════════════════
# AUTH ROUTES
# ═══════════════════════════════════════════════════════════════

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
        
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if User.query.filter_by(username=username).first():
            flash("Bu ismdagi foydalanuvchi allaqachon mavjud!", "danger")
            return redirect(url_for('register'))
            
        user = User(username=username, role='student')
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        
        login_user(user)
        flash("Muvaffaqiyatli ro'yxatdan o'tdingiz!", "success")
        return redirect(url_for('index'))
        
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
        
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            flash("Xush kelibsiz, " + user.username + "!", "success")
            # Return to previous page if needed
            next_page = request.args.get('next')
            return redirect(next_page if next_page else url_for('index'))
        else:
            flash("Login yoki parol noto'g'ri!", "danger")
            
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Tizimdan chiqdingiz.", "info")
    return redirect(url_for('index'))

# ═══════════════════════════════════════════════════════════════
# PUBLIC ROUTES
# ═══════════════════════════════════════════════════════════════

@app.route('/')
def index():
    """Bosh sahifa"""
    modules = Module.query.order_by(Module.order).all()
    total_lessons = Lesson.query.count()
    total_tests = Test.query.count()
    total_assignments = Assignment.query.count()

    return render_template('index.html',
                           modules=modules,
                           total_lessons=total_lessons,
                           total_tests=total_tests,
                           total_assignments=total_assignments)


@app.route('/modules')
def modules_page():
    """Barcha modullar"""
    modules = Module.query.order_by(Module.order).all()
    return render_template('modules.html', modules=modules)


@app.route('/module/<int:module_id>')
def module_detail(module_id):
    """Modul tafsilotlari"""
    module = Module.query.get_or_404(module_id)
    return render_template('module_detail.html', module=module)


@app.route('/lesson/<int:lesson_id>')
def lesson_page(lesson_id):
    """Dars sahifasi"""
    lesson = Lesson.query.get_or_404(lesson_id)
    lessons = Lesson.query.filter_by(module_id=lesson.module_id).order_by(Lesson.order).all()

    # Oldingi va keyingi darslar
    prev_lesson = None
    next_lesson = None
    for i, l in enumerate(lessons):
        if l.id == lesson.id:
            if i > 0:
                prev_lesson = lessons[i - 1]
            if i < len(lessons) - 1:
                next_lesson = lessons[i + 1]
            break

    return render_template('lesson.html',
                           lesson=lesson,
                           lessons=lessons,
                           prev_lesson=prev_lesson,
                           next_lesson=next_lesson)


@app.route('/test/<int:module_id>')
def test_page(module_id):
    """Test sahifasi"""
    module = Module.query.get_or_404(module_id)
    tests = Test.query.filter_by(module_id=module_id).all()

    tests_data = [t.to_dict() for t in tests]

    return render_template('test.html',
                           module=module,
                           tests=tests,
                           tests_json=json.dumps(tests_data, ensure_ascii=False))


@app.route('/assignment/<int:assignment_id>')
def assignment_page(assignment_id):
    """Topshiriq sahifasi"""
    assignment = Assignment.query.get_or_404(assignment_id)
    submissions = Submission.query.filter_by(assignment_id=assignment_id) \
        .order_by(Submission.submitted_at.desc()).all()

    return render_template('assignment.html',
                           assignment=assignment,
                           submissions=submissions)


@app.route('/submit/<int:assignment_id>', methods=['POST'])
@login_required
def submit_assignment(assignment_id):
    """Topshiriq yuborish — fayl yuklash va AI tekshirish"""
    assignment = Assignment.query.get_or_404(assignment_id)

    if 'file' not in request.files:
        flash('Fayl tanlanmadi!', 'danger')
        return redirect(url_for('assignment_page', assignment_id=assignment_id))

    file = request.files['file']
    if file.filename == '':
        flash('Fayl tanlanmadi!', 'danger')
        return redirect(url_for('assignment_page', assignment_id=assignment_id))

    if not allowed_file(file.filename):
        flash('Bu fayl formati qo\'llab-quvvatlanmaydi!', 'danger')
        return redirect(url_for('assignment_page', assignment_id=assignment_id))

    # Faylni saqlash
    filename = secure_filename(file.filename)
    # Unique filename
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    safe_filename = f"{timestamp}_{filename}"
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], safe_filename)
    file.save(filepath)

    file_ext = filename.rsplit('.', 1)[1].lower()

    # Submission yaratish
    submission = Submission(
        file_path=filepath,
        file_name=filename,
        file_type=file_ext,
        status='processing',
        assignment_id=assignment_id,
    )
    db.session.add(submission)
    db.session.commit()

    # AI tekshirishni background thread da ishga tushirish
    submission_id = submission.id
    thread = threading.Thread(
        target=process_submission_async,
        args=(app, submission_id, filepath, filename, file_ext,
              assignment.title, assignment.description)
    )
    thread.daemon = True
    thread.start()

    return redirect(url_for('submission_result', submission_id=submission_id))


def process_submission_async(flask_app, submission_id, filepath, filename, file_ext,
                             assignment_title, assignment_description):
    """Background thread da AI tekshirish"""
    with flask_app.app_context():
        try:
            result = evaluate_submission(
                filepath=filepath,
                filename=filename,
                file_type=file_ext,
                assignment_title=assignment_title,
                assignment_description=assignment_description,
            )

            submission = Submission.query.get(submission_id)
            if submission:
                submission.score = result.get('score', 0)
                submission.feedback = result.get('feedback', '')
                submission.strengths = result.get('strengths', '')
                submission.weaknesses = result.get('weaknesses', '')
                submission.recommendations = result.get('recommendations', '')
                submission.detailed_analysis = result.get('detailed_analysis', '')
                submission.status = result.get('status', 'completed')
                submission.evaluated_at = datetime.utcnow()
                db.session.commit()

        except Exception as e:
            submission = Submission.query.get(submission_id)
            if submission:
                submission.status = 'error'
                submission.feedback = f'Xatolik: {str(e)}'
                db.session.commit()


@app.route('/result/<int:submission_id>')
def submission_result(submission_id):
    """AI tekshiruv natijasi"""
    submission = Submission.query.get_or_404(submission_id)

    # Agar hali tekshirilmagan bo'lsa
    if submission.status in ('pending', 'processing'):
        return render_template('submission_loading.html', submission=submission)

    return render_template('submission_result.html', submission=submission)


@app.route('/api/submission-status/<int:submission_id>')
@login_required
def check_submission_status(submission_id):
    """AJAX: Submission holatini tekshirish"""
    submission = Submission.query.get_or_404(submission_id)
    return jsonify({
        'status': submission.status,
        'score': submission.score,
    })


# ═══════════════════════════════════════════════════════════════
# ADMIN ROUTES
# ═══════════════════════════════════════════════════════════════

@app.route('/admin')
@admin_required
def admin_page():
    """Admin panel"""
    modules = Module.query.order_by(Module.order).all()
    lessons = Lesson.query.order_by(Lesson.module_id, Lesson.order).all()
    tests = Test.query.order_by(Test.module_id).all()
    assignments = Assignment.query.order_by(Assignment.module_id).all()

    return render_template('admin.html',
                           modules=modules,
                           lessons=lessons,
                           tests=tests,
                           assignments=assignments)


# ── Module API ───────────────────────────────────────────────────
@app.route('/api/admin/modules', methods=['POST'])
@admin_required
def create_module():
    data = request.get_json()
    module = Module(
        title=data['title'],
        description=data.get('description', ''),
        icon=data.get('icon', '📚'),
        order=Module.query.count() + 1,
    )
    db.session.add(module)
    db.session.commit()
    return jsonify(module.to_dict()), 201


@app.route('/api/admin/modules/<int:module_id>', methods=['PUT'])
@admin_required
def update_module(module_id):
    module = Module.query.get_or_404(module_id)
    data = request.get_json()
    module.title = data.get('title', module.title)
    module.description = data.get('description', module.description)
    module.icon = data.get('icon', module.icon)
    db.session.commit()
    return jsonify(module.to_dict())


@app.route('/api/admin/modules/<int:module_id>', methods=['DELETE'])
@admin_required
def delete_module(module_id):
    module = Module.query.get_or_404(module_id)
    db.session.delete(module)
    db.session.commit()
    return jsonify({'message': 'O\'chirildi'}), 200


# ── Lesson API ───────────────────────────────────────────────────
@app.route('/api/admin/lessons', methods=['POST'])
@admin_required
def create_lesson():
    data = request.get_json()
    lesson_count = Lesson.query.filter_by(module_id=data['module_id']).count()
    lesson = Lesson(
        title=data['title'],
        description=data.get('description', ''),
        video_url=data.get('video_url', ''),
        duration=data.get('duration', '00:00'),
        order=lesson_count + 1,
        module_id=data['module_id'],
    )
    db.session.add(lesson)
    db.session.commit()
    return jsonify(lesson.to_dict()), 201


@app.route('/api/admin/lessons/<int:lesson_id>', methods=['PUT'])
@admin_required
def update_lesson(lesson_id):
    lesson = Lesson.query.get_or_404(lesson_id)
    data = request.get_json()
    lesson.title = data.get('title', lesson.title)
    lesson.description = data.get('description', lesson.description)
    lesson.video_url = data.get('video_url', lesson.video_url)
    lesson.duration = data.get('duration', lesson.duration)
    lesson.module_id = data.get('module_id', lesson.module_id)
    db.session.commit()
    return jsonify(lesson.to_dict())


@app.route('/api/admin/lessons/<int:lesson_id>', methods=['DELETE'])
@admin_required
def delete_lesson(lesson_id):
    lesson = Lesson.query.get_or_404(lesson_id)
    db.session.delete(lesson)
    db.session.commit()
    return jsonify({'message': 'O\'chirildi'}), 200


# ── Test API ─────────────────────────────────────────────────────
@app.route('/api/admin/tests', methods=['POST'])
@admin_required
def create_test():
    data = request.get_json()
    test = Test(
        question=data['question'],
        option_a=data['option_a'],
        option_b=data['option_b'],
        option_c=data['option_c'],
        option_d=data['option_d'],
        correct_answer=data['correct_answer'],
        explanation=data.get('explanation', ''),
        module_id=data['module_id'],
    )
    db.session.add(test)
    db.session.commit()
    return jsonify(test.to_dict()), 201


@app.route('/api/admin/tests/<int:test_id>', methods=['PUT'])
@admin_required
def update_test(test_id):
    test = Test.query.get_or_404(test_id)
    data = request.get_json()
    test.question = data.get('question', test.question)
    test.option_a = data.get('option_a', test.option_a)
    test.option_b = data.get('option_b', test.option_b)
    test.option_c = data.get('option_c', test.option_c)
    test.option_d = data.get('option_d', test.option_d)
    test.correct_answer = data.get('correct_answer', test.correct_answer)
    test.explanation = data.get('explanation', test.explanation)
    test.module_id = data.get('module_id', test.module_id)
    db.session.commit()
    return jsonify(test.to_dict())


@app.route('/api/admin/tests/<int:test_id>', methods=['DELETE'])
@admin_required
def delete_test(test_id):
    test = Test.query.get_or_404(test_id)
    db.session.delete(test)
    db.session.commit()
    return jsonify({'message': 'O\'chirildi'}), 200


# ── Assignment API ───────────────────────────────────────────────
@app.route('/api/admin/assignments', methods=['POST'])
@admin_required
def create_assignment():
    data = request.get_json()
    assignment = Assignment(
        title=data['title'],
        description=data.get('description', ''),
        assignment_type=data.get('assignment_type', 'document'),
        accepted_formats=data.get('accepted_formats', 'pdf,docx,pptx'),
        module_id=data['module_id'],
    )
    db.session.add(assignment)
    db.session.commit()
    return jsonify(assignment.to_dict()), 201


@app.route('/api/admin/assignments/<int:assignment_id>', methods=['PUT'])
@admin_required
def update_assignment(assignment_id):
    assignment = Assignment.query.get_or_404(assignment_id)
    data = request.get_json()
    assignment.title = data.get('title', assignment.title)
    assignment.description = data.get('description', assignment.description)
    assignment.assignment_type = data.get('assignment_type', assignment.assignment_type)
    assignment.accepted_formats = data.get('accepted_formats', assignment.accepted_formats)
    assignment.module_id = data.get('module_id', assignment.module_id)
    db.session.commit()
    return jsonify(assignment.to_dict())


@app.route('/api/admin/assignments/<int:assignment_id>', methods=['DELETE'])
@admin_required
def delete_assignment(assignment_id):
    assignment = Assignment.query.get_or_404(assignment_id)
    db.session.delete(assignment)
    db.session.commit()
    return jsonify({'message': 'O\'chirildi'}), 200


# ═══════════════════════════════════════════════════════════════
# APP STARTUP
# ═══════════════════════════════════════════════════════════════

with app.app_context():
    db.create_all()
    seed_database()


if __name__ == '__main__':
    app.run(debug=True, port=5000)
