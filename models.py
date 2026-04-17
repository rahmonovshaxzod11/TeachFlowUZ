"""
TeachFlowUZ — Database Models
SQLAlchemy modellari: Module, Lesson, Test, Assignment, Submission
"""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class User(UserMixin, db.Model):
    """Foydalanuvchi modeli (Student, Admin)"""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), default='student')  # 'admin' or 'student'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def is_admin(self):
        return self.role == 'admin'


class Module(db.Model):
    """Modul — ta'lim moduli (masalan: Pedagogika asoslari)"""
    __tablename__ = 'modules'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    icon = db.Column(db.String(10), default='📚')  # Emoji icon
    order = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    lessons = db.relationship('Lesson', backref='module', lazy=True, cascade='all, delete-orphan', order_by='Lesson.order')
    tests = db.relationship('Test', backref='module', lazy=True, cascade='all, delete-orphan')
    assignments = db.relationship('Assignment', backref='module', lazy=True, cascade='all, delete-orphan')

    def lesson_count(self):
        return len(self.lessons)

    def test_count(self):
        return len(self.tests)

    def assignment_count(self):
        return len(self.assignments)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'icon': self.icon,
            'order': self.order,
            'lesson_count': self.lesson_count(),
            'test_count': self.test_count(),
            'assignment_count': self.assignment_count(),
        }


class Lesson(db.Model):
    """Dars — video dars"""
    __tablename__ = 'lessons'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    video_url = db.Column(db.String(500), nullable=True)  # YouTube embed URL or local path
    duration = db.Column(db.String(20), default='00:00')  # "15:30" format
    order = db.Column(db.Integer, default=0)
    module_id = db.Column(db.Integer, db.ForeignKey('modules.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'video_url': self.video_url,
            'duration': self.duration,
            'order': self.order,
            'module_id': self.module_id,
        }


class Test(db.Model):
    """Test savoli — modulga tegishli"""
    __tablename__ = 'tests'

    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.Text, nullable=False)
    option_a = db.Column(db.String(300), nullable=False)
    option_b = db.Column(db.String(300), nullable=False)
    option_c = db.Column(db.String(300), nullable=False)
    option_d = db.Column(db.String(300), nullable=False)
    correct_answer = db.Column(db.String(1), nullable=False)  # 'a', 'b', 'c', or 'd'
    explanation = db.Column(db.Text, nullable=True)  # Javob izohi
    module_id = db.Column(db.Integer, db.ForeignKey('modules.id'), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'question': self.question,
            'option_a': self.option_a,
            'option_b': self.option_b,
            'option_c': self.option_c,
            'option_d': self.option_d,
            'correct_answer': self.correct_answer,
            'explanation': self.explanation,
            'module_id': self.module_id,
        }


class Assignment(db.Model):
    """Topshiriq — modulga tegishli vazifa"""
    __tablename__ = 'assignments'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    assignment_type = db.Column(db.String(50), default='document')  # 'document', 'video', 'presentation'
    accepted_formats = db.Column(db.String(200), default='pdf,docx,pptx')
    module_id = db.Column(db.Integer, db.ForeignKey('modules.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    submissions = db.relationship('Submission', backref='assignment', lazy=True, cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'assignment_type': self.assignment_type,
            'accepted_formats': self.accepted_formats,
            'module_id': self.module_id,
        }


class Submission(db.Model):
    """Yuborilgan ish — talaba tomonidan yuborilgan fayl va AI bahosi"""
    __tablename__ = 'submissions'

    id = db.Column(db.Integer, primary_key=True)
    file_path = db.Column(db.String(500), nullable=False)
    file_name = db.Column(db.String(200), nullable=False)
    file_type = db.Column(db.String(20), nullable=False)  # 'pdf', 'docx', 'pptx', 'mp4'

    # AI evaluation results
    score = db.Column(db.Float, nullable=True)  # 0-100
    feedback = db.Column(db.Text, nullable=True)  # JSON formatted feedback
    strengths = db.Column(db.Text, nullable=True)  # Kuchli tomonlar
    weaknesses = db.Column(db.Text, nullable=True)  # Zaif tomonlar
    recommendations = db.Column(db.Text, nullable=True)  # Tavsiyalar
    detailed_analysis = db.Column(db.Text, nullable=True)  # Batafsil tahlil

    status = db.Column(db.String(20), default='pending')  # 'pending', 'processing', 'completed', 'error'
    assignment_id = db.Column(db.Integer, db.ForeignKey('assignments.id'), nullable=False)
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)
    evaluated_at = db.Column(db.DateTime, nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'file_name': self.file_name,
            'file_type': self.file_type,
            'score': self.score,
            'feedback': self.feedback,
            'strengths': self.strengths,
            'weaknesses': self.weaknesses,
            'recommendations': self.recommendations,
            'detailed_analysis': self.detailed_analysis,
            'status': self.status,
            'assignment_id': self.assignment_id,
            'submitted_at': self.submitted_at.isoformat() if self.submitted_at else None,
            'evaluated_at': self.evaluated_at.isoformat() if self.evaluated_at else None,
        }
