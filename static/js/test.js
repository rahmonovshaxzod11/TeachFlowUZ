/**
 * TeachFlowUZ — Test Logic
 * Test navigation, answer checking, scoring
 */

class TestEngine {
    constructor(questions) {
        this.questions = questions;
        this.currentIndex = 0;
        this.answers = {};
        this.submitted = false;
        this.init();
    }

    init() {
        this.renderQuestion();
        this.updateProgress();
        this.updateNavButtons();
    }

    renderQuestion() {
        const q = this.questions[this.currentIndex];
        const container = document.getElementById('test-question-area');
        if (!container) return;

        const selectedAnswer = this.answers[this.currentIndex];

        container.innerHTML = `
            <div class="test-question-card animate-fade-in-up">
                <div class="test-question-number">Savol ${this.currentIndex + 1} / ${this.questions.length}</div>
                <div class="test-question-text">${q.question}</div>
                <div class="test-options">
                    ${['a', 'b', 'c', 'd'].map(letter => `
                        <div class="test-option ${selectedAnswer === letter ? 'selected' : ''} ${this.submitted ? (letter === q.correct_answer ? 'correct' : (selectedAnswer === letter ? 'wrong' : '')) : ''}"
                             onclick="${this.submitted ? '' : `testEngine.selectAnswer('${letter}')`}"
                             id="option-${letter}">
                            <span class="test-option-letter">${letter.toUpperCase()}</span>
                            <span class="test-option-text">${q['option_' + letter]}</span>
                        </div>
                    `).join('')}
                </div>
                ${this.submitted && q.explanation ? `
                    <div class="test-explanation visible">
                        <strong>💡 Izoh:</strong> ${q.explanation}
                    </div>
                ` : ''}
            </div>
        `;
    }

    selectAnswer(letter) {
        if (this.submitted) return;
        this.answers[this.currentIndex] = letter;
        this.renderQuestion();
        this.updateProgress();
    }

    nextQuestion() {
        if (this.currentIndex < this.questions.length - 1) {
            this.currentIndex++;
            this.renderQuestion();
            this.updateProgress();
            this.updateNavButtons();
        }
    }

    prevQuestion() {
        if (this.currentIndex > 0) {
            this.currentIndex--;
            this.renderQuestion();
            this.updateProgress();
            this.updateNavButtons();
        }
    }

    updateProgress() {
        const answered = Object.keys(this.answers).length;
        const total = this.questions.length;
        const percent = (answered / total) * 100;

        const fill = document.getElementById('test-progress-fill');
        const text = document.getElementById('test-progress-text');

        if (fill) fill.style.width = `${percent}%`;
        if (text) text.textContent = `${answered} / ${total}`;
    }

    updateNavButtons() {
        const prevBtn = document.getElementById('test-prev-btn');
        const nextBtn = document.getElementById('test-next-btn');
        const submitBtn = document.getElementById('test-submit-btn');

        if (prevBtn) prevBtn.disabled = this.currentIndex === 0;

        if (nextBtn && submitBtn) {
            if (this.currentIndex === this.questions.length - 1) {
                nextBtn.style.display = 'none';
                submitBtn.style.display = this.submitted ? 'none' : 'inline-flex';
            } else {
                nextBtn.style.display = 'inline-flex';
                submitBtn.style.display = 'none';
            }
        }
    }

    submitTest() {
        const answered = Object.keys(this.answers).length;
        if (answered < this.questions.length) {
            if (!confirm(`Siz hali ${this.questions.length - answered} ta savolga javob bermadingiz. Davom etasizmi?`)) {
                return;
            }
        }

        this.submitted = true;
        this.currentIndex = 0;

        // Calculate score
        let correct = 0;
        this.questions.forEach((q, idx) => {
            if (this.answers[idx] === q.correct_answer) {
                correct++;
            }
        });

        this.score = correct;
        this.showResults();
    }

    showResults() {
        const total = this.questions.length;
        const correct = this.score;
        const percent = Math.round((correct / total) * 100);

        let message = '';
        let messageClass = '';
        if (percent >= 90) {
            message = "A'lo natija! 🎉";
            messageClass = 'excellent';
        } else if (percent >= 70) {
            message = "Yaxshi natija! 👍";
            messageClass = 'good';
        } else if (percent >= 50) {
            message = "O'rtacha natija 📖";
            messageClass = 'average';
        } else {
            message = "Ko'proq tayyorlanish kerak 💪";
            messageClass = 'poor';
        }

        const container = document.getElementById('test-area');
        if (!container) return;

        container.innerHTML = `
            <div class="test-results animate-fade-in-up">
                <div class="test-results-score">
                    <div class="test-results-circle" style="--score-deg: ${percent * 3.6}deg">
                        <span class="test-results-value">${percent}%</span>
                    </div>
                </div>
                <div class="test-results-label">${correct} / ${total} to'g'ri javob</div>
                <div class="test-results-message ${messageClass}">${message}</div>
                <div style="display:flex;gap:12px;justify-content:center;flex-wrap:wrap;">
                    <button class="btn btn-primary" onclick="testEngine.reviewAnswers()">
                        📋 Javoblarni ko'rish
                    </button>
                    <button class="btn btn-secondary" onclick="location.reload()">
                        🔄 Qayta topshirish
                    </button>
                </div>
            </div>
        `;
    }

    reviewAnswers() {
        this.currentIndex = 0;

        const container = document.getElementById('test-area');
        if (!container) return;

        container.innerHTML = `
            <div class="test-progress">
                <div class="test-progress-bar">
                    <div class="test-progress-fill" id="test-progress-fill" style="width: 100%"></div>
                </div>
                <span class="test-progress-text" id="test-progress-text">${this.questions.length} / ${this.questions.length}</span>
            </div>
            <div id="test-question-area"></div>
            <div class="test-actions">
                <button class="btn btn-secondary" id="test-prev-btn" onclick="testEngine.prevQuestion()">
                    ← Oldingi
                </button>
                <button class="btn btn-primary" id="test-next-btn" onclick="testEngine.nextQuestion()">
                    Keyingi →
                </button>
                <button class="btn btn-success" id="test-submit-btn" style="display:none;" onclick="testEngine.submitTest()">
                    ✅ Yakunlash
                </button>
            </div>
        `;

        this.renderQuestion();
        this.updateNavButtons();
    }
}

let testEngine = null;

function initTest(questions) {
    testEngine = new TestEngine(questions);
}
