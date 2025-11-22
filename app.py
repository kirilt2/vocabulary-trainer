from flask import Flask, render_template_string, request, redirect, url_for, session
import random

app = Flask(__name__)
app.secret_key = "CHANGE_THIS_SECRET_KEY_12345"

# ==================== CSS STYLES ====================
CSS_STYLES = """
* {
    box-sizing: border-box;
}

body {
    margin: 0;
    font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    background: radial-gradient(circle at top, #2b2d42 0, #000 55%);
    color: #f8f8ff;
    min-height: 100vh;
}

.container {
    width: 100%;
    max-width: 1100px;
    margin: 0 auto;
    padding: 0 1rem;
}

.site-header {
    backdrop-filter: blur(12px);
    background: rgba(15, 15, 30, 0.85);
    border-bottom: 1px solid rgba(255, 255, 255, 0.06);
    position: sticky;
    top: 0;
    z-index: 50;
}

.header-content {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0.8rem 0;
}

.logo {
    font-size: 1.2rem;
    margin: 0;
}

.nav a {
    color: #eee;
    margin-left: 1rem;
    text-decoration: none;
    font-size: 0.95rem;
    padding: 0.35rem 0.7rem;
    border-radius: 999px;
    transition: background 0.2s, transform 0.1s;
}

.nav a:hover {
    background: rgba(255, 255, 255, 0.08);
    transform: translateY(-1px);
}

.main-content {
    padding: 2rem 0 3rem;
}

.site-footer {
    border-top: 1px solid rgba(255, 255, 255, 0.06);
    background: rgba(10, 10, 20, 0.9);
    padding: 1rem 0;
    text-align: center;
    font-size: 0.85rem;
}

/* HERO */
.hero {
    text-align: center;
    margin-bottom: 2rem;
}

.hero h2 {
    margin-bottom: 0.5rem;
}

.hero p {
    opacity: 0.85;
}

.hero-buttons {
    margin-top: 1.5rem;
    display: flex;
    gap: 1rem;
    justify-content: center;
    flex-wrap: wrap;
}

/* BUTTONS */
.btn {
    border: 1px solid rgba(255, 255, 255, 0.3);
    padding: 0.6rem 1.3rem;
    border-radius: 999px;
    background: transparent;
    color: #fff;
    text-decoration: none;
    font-size: 0.95rem;
    cursor: pointer;
    display: inline-block;
    transition: background 0.2s, transform 0.1s, box-shadow 0.2s;
}

.btn.primary {
    border-color: #ff7513;
    background: linear-gradient(135deg, #ff7513, #ffb347);
    color: #000;
    font-weight: 600;
}

.btn.secondary {
    border-color: #4cc9f0;
}

.btn:hover {
    transform: translateY(-1px);
    box-shadow: 0 8px 20px rgba(0, 0, 0, 0.35);
}

/* SUBTITLE */
.subtitle {
    opacity: 0.8;
    margin-bottom: 1.5rem;
    text-align: center;
}

.result-summary {
    text-align: center;
    font-size: 1.2rem;
    margin: 1.5rem 0;
}

/* FLASHCARDS */
.flashcard-container {
    max-width: 600px;
    margin: 2rem auto;
}

.card-display {
    position: relative;
    min-height: 350px;
    margin-bottom: 2rem;
}

.flashcard {
    background: radial-gradient(circle at top left, #ff7513 0, #141424 70%);
    border-radius: 20px;
    padding: 3rem 2rem;
    text-align: center;
    border: 2px solid rgba(255, 255, 255, 0.1);
    min-height: 300px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    box-shadow: 0 10px 40px rgba(0, 0, 0, 0.4);
    cursor: pointer;
    transition: transform 0.2s, box-shadow 0.2s;
    user-select: none;
}

.flashcard:hover {
    transform: translateY(-5px);
    box-shadow: 0 15px 50px rgba(0, 0, 0, 0.5);
}

.flashcard:active {
    transform: translateY(-2px);
}

.flashcard .card-number {
    position: absolute;
    top: 1rem;
    right: 1rem;
    font-size: 0.85rem;
    opacity: 0.7;
    background: rgba(0, 0, 0, 0.3);
    padding: 0.3rem 0.8rem;
    border-radius: 999px;
}

.flashcard .english-text {
    font-size: 1.8rem;
    font-weight: 600;
    margin-bottom: 1.5rem;
    color: #fff;
}

.flashcard .hebrew-text {
    font-size: 1.5rem;
    margin-top: 1rem;
    padding-top: 1rem;
    border-top: 2px solid rgba(255, 255, 255, 0.2);
    color: #4cc9f0;
    min-height: 60px;
    display: flex;
    align-items: center;
    justify-content: center;
}

.flashcard .hebrew-text.hidden {
    opacity: 0;
    visibility: hidden;
}

.flashcard .tap-hint {
    font-size: 0.9rem;
    margin-top: 1rem;
    opacity: 0.6;
    animation: pulse 2s ease-in-out infinite;
}

.flashcard .tap-hint.hidden {
    display: none;
}

@keyframes pulse {
    0%, 100% {
        opacity: 0.6;
    }
    50% {
        opacity: 1;
    }
}

.flashcard-controls {
    display: flex;
    gap: 1rem;
    justify-content: center;
    align-items: center;
    margin-top: 2rem;
}

.nav-btn {
    background: rgba(255, 255, 255, 0.1);
    border: 1px solid rgba(255, 255, 255, 0.3);
    color: #fff;
    font-size: 1.5rem;
    width: 50px;
    height: 50px;
    border-radius: 50%;
    cursor: pointer;
    transition: all 0.2s;
    display: flex;
    align-items: center;
    justify-content: center;
}

.nav-btn:hover:not(:disabled) {
    background: rgba(255, 255, 255, 0.2);
    transform: scale(1.1);
}

.nav-btn:disabled {
    opacity: 0.3;
    cursor: not-allowed;
}

.show-answer-btn {
    padding: 0.8rem 2rem;
    font-size: 1rem;
    background: linear-gradient(135deg, #4cc9f0, #3a9fb8);
    border: none;
    border-radius: 999px;
    color: #000;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s;
}

.show-answer-btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 5px 20px rgba(76, 201, 240, 0.4);
}

.progress-indicator {
    text-align: center;
    margin-top: 1.5rem;
    font-size: 0.9rem;
    opacity: 0.8;
}

.progress-bar {
    width: 100%;
    height: 8px;
    background: rgba(255, 255, 255, 0.1);
    border-radius: 999px;
    margin-top: 0.5rem;
    overflow: hidden;
}

.progress-fill {
    height: 100%;
    background: linear-gradient(90deg, #ff7513, #4cc9f0);
    border-radius: 999px;
    transition: width 0.3s ease;
}

/* QUIZ */
.quiz-form {
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
}

.quiz-question {
    padding: 1rem;
    border-radius: 12px;
    background: rgba(15, 15, 30, 0.9);
    border: 1px solid rgba(255, 255, 255, 0.08);
}

.quiz-question h3 {
    margin-top: 0;
    margin-bottom: 0.6rem;
    font-size: 1rem;
}

.options {
    display: flex;
    flex-direction: column;
    gap: 0.4rem;
}

.option {
    display: flex;
    align-items: center;
    gap: 0.4rem;
    font-size: 0.95rem;
    cursor: pointer;
}

.option input[type="radio"] {
    transform: scale(1.1);
}

/* RESULTS */
.results-table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 1.5rem;
    font-size: 0.9rem;
}

.results-table th,
.results-table td {
    border: 1px solid rgba(255, 255, 255, 0.1);
    padding: 0.5rem;
    text-align: right;
}

.results-table th {
    background: rgba(255, 255, 255, 0.05);
}

.results-table tr.correct {
    background: rgba(0, 150, 0, 0.15);
}

.results-table tr.wrong {
    background: rgba(200, 0, 0, 0.2);
}

/* RESPONSIVE */
@media (max-width: 600px) {
    .header-content {
        flex-direction: column;
        align-items: flex-start;
        gap: 0.4rem;
    }

    .nav {
        width: 100%;
        display: flex;
        gap: 0.5rem;
        flex-wrap: wrap;
    }

    .nav a {
        flex: 1 1 auto;
        text-align: center;
        margin-left: 0;
    }

    .flashcard .english-text {
        font-size: 1.4rem;
    }

    .flashcard .hebrew-text {
        font-size: 1.2rem;
    }

    .flashcard {
        padding: 2rem 1.5rem;
        min-height: 250px;
    }

    .quiz-question h3 {
        font-size: 0.95rem;
    }

    .option {
        font-size: 0.9rem;
    }

    .hero h2 {
        font-size: 1.5rem;
    }

    .results-table {
        font-size: 0.8rem;
    }

    .results-table th,
    .results-table td {
        padding: 0.4rem;
    }
}
"""

# ==================== HTML TEMPLATES ====================
BASE_TEMPLATE = """
<!DOCTYPE html>
<html lang="he" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}אוצר מילים - Quiz{% endblock %}</title>
    <style>{{ css|safe }}</style>
</head>
<body>
<header class="site-header">
    <div class="container header-content">
        <h1 class="logo">📚 Vocabulary Trainer</h1>
        <nav class="nav">
            <a href="/">דף הבית</a>
            <a href="/flashcards">כרטיסיות</a>
            <a href="/quiz">Quiz אקראי</a>
        </nav>
    </div>
</header>

<main class="container main-content">
    {% block content %}{% endblock %}
</main>

</body>
</html>
"""

INDEX_TEMPLATE = BASE_TEMPLATE.replace(
    "{% block content %}{% endblock %}",
    """
<section class="hero">
    <h2>לימוד מילים למבחן באנגלית</h2>
    <p>יש לך {{ total }} מילים. אפשר לתרגל בכרטיסיות או לעשות Quiz עם 20 מילים אקראיות.</p>
    
    <div class="hero-buttons">
        <a class="btn primary" href="/flashcards">כרטיסיות אנגלית ↔ עברית</a>
        <a class="btn secondary" href="/quiz">התחל Quiz של 50 מילים</a>
    </div>
</section>
"""
)

FLASHCARDS_TEMPLATE = BASE_TEMPLATE.replace(
    "{% block content %}{% endblock %}",
    """
<div class="flashcard-container">
    <h2>כרטיסיות – לחץ על הכרטיס כדי לראות את התרגום</h2>
    <p class="subtitle">השתמש בחצים כדי לנווט בין המילים או החלק ימינה/שמאלה</p>

    <div class="card-display">
        <div class="flashcard" id="flashcard" onclick="toggleAnswer()">
            <div class="card-number" id="cardNumber">1 / {{ words|length }}</div>
            <div class="english-text" id="englishText">{{ words[0].english }}</div>
            <div class="hebrew-text hidden" id="hebrewText">{{ words[0].hebrew }}</div>
            <div class="tap-hint" id="tapHint">👆 לחץ כדי לראות תרגום</div>
        </div>
    </div>

    <div class="flashcard-controls">
        <button class="nav-btn" id="prevBtn" onclick="prevCard()">←</button>
        <button class="nav-btn" id="nextBtn" onclick="nextCard()">→</button>
    </div>

    <div class="progress-indicator">
        <div class="progress-bar">
            <div class="progress-fill" id="progressFill" style="width: {{ (1 / words|length * 100)|round }}%"></div>
        </div>
    </div>
</div>

<script>
const words = {{ words|tojson }};
let currentIndex = 0;

const englishText = document.getElementById('englishText');
const hebrewText = document.getElementById('hebrewText');
const cardNumber = document.getElementById('cardNumber');
const tapHint = document.getElementById('tapHint');
const prevBtn = document.getElementById('prevBtn');
const nextBtn = document.getElementById('nextBtn');
const progressFill = document.getElementById('progressFill');

function updateCard() {
    const word = words[currentIndex];
    englishText.textContent = word.english;
    hebrewText.textContent = word.hebrew;
    hebrewText.classList.add('hidden');
    tapHint.classList.remove('hidden');
    cardNumber.textContent = `${currentIndex + 1} / ${words.length}`;
    
    // Update progress bar
    progressFill.style.width = `${((currentIndex + 1) / words.length) * 100}%`;
    
    // Update button states
    prevBtn.disabled = currentIndex === 0;
    nextBtn.disabled = currentIndex === words.length - 1;
}

function toggleAnswer() {
    hebrewText.classList.toggle('hidden');
    tapHint.classList.toggle('hidden');
}

function nextCard() {
    if (currentIndex < words.length - 1) {
        currentIndex++;
        updateCard();
    }
}

function prevCard() {
    if (currentIndex > 0) {
        currentIndex--;
        updateCard();
    }
}

// Keyboard navigation
document.addEventListener('keydown', function(event) {
    if (event.key === 'ArrowRight' || event.key === 'ArrowDown') {
        nextCard();
    } else if (event.key === 'ArrowLeft' || event.key === 'ArrowUp') {
        prevCard();
    } else if (event.key === ' ' || event.key === 'Enter') {
        event.preventDefault();
        toggleAnswer();
    }
});

// Touch swipe support
let touchStartX = 0;
let touchEndX = 0;
let touchStartY = 0;
let touchEndY = 0;

const flashcard = document.getElementById('flashcard');

flashcard.addEventListener('touchstart', function(event) {
    touchStartX = event.changedTouches[0].screenX;
    touchStartY = event.changedTouches[0].screenY;
});

flashcard.addEventListener('touchend', function(event) {
    touchEndX = event.changedTouches[0].screenX;
    touchEndY = event.changedTouches[0].screenY;
    handleSwipe();
});

function handleSwipe() {
    const xDiff = touchStartX - touchEndX;
    const yDiff = touchStartY - touchEndY;
    
    // Only handle swipe if horizontal movement is greater than vertical
    if (Math.abs(xDiff) > Math.abs(yDiff) && Math.abs(xDiff) > 50) {
        if (xDiff > 0) {
            // Swipe left - next card
            nextCard();
        } else {
            // Swipe right - previous card
            prevCard();
        }
    } else if (Math.abs(xDiff) < 30 && Math.abs(yDiff) < 30) {
        // Tap (no significant swipe) - toggle answer
        toggleAnswer();
    }
}

// Initialize
updateCard();
</script>
"""
)

QUIZ_TEMPLATE = BASE_TEMPLATE.replace(
    "{% block content %}{% endblock %}",
    """
<h2>Quiz – 50 מילים אקראיות</h2>
<p class="subtitle">בחר את התרגום הנכון לעברית לכל מילה באנגלית.</p>

<form method="post" class="quiz-form">
    {% for q in questions %}
    <div class="quiz-question">
        <h3>{{ loop.index }}. {{ q.english }}</h3>
        <div class="options">
            {% for option in q.options %}
            <label class="option">
                <input type="radio" name="{{ q.id }}" value="{{ option }}" required>
                <span>{{ option }}</span>
            </label>
            {% endfor %}
        </div>
    </div>
    {% endfor %}
    
    <button type="submit" class="btn primary">בדיקת תשובות</button>
</form>
"""
)

QUIZ_RESULT_TEMPLATE = BASE_TEMPLATE.replace(
    "{% block content %}{% endblock %}",
    """
<h2>תוצאות ה-Quiz</h2>
<p class="subtitle">
    קיבלת {{ correct }} מתוך {{ total }} – ציון {{ score }}%.
</p>

<div class="result-summary">
    {% if score >= 85 %}
        <p>🔥 מצוין! אתה שולט בחומר.</p>
    {% elif score >= 60 %}
        <p>😊 יפה! אבל שווה לעבור שוב על המילים החלשות.</p>
    {% else %}
        <p>🧠 לא נורא, לומדים מתרגול. נסה שוב עוד Quiz!</p>
    {% endif %}
</div>

<table class="results-table">
    <thead>
        <tr>
            <th>מילה באנגלית</th>
            <th>התרגום הנכון</th>
            <th>התשובה שלך</th>
            <th>נכון?</th>
        </tr>
    </thead>
    <tbody>
        {% for row in details %}
        <tr class="{{ 'correct' if row.is_correct else 'wrong' }}">
            <td>{{ row.english }}</td>
            <td>{{ row.correct_hebrew }}</td>
            <td>{{ row.chosen_hebrew }}</td>
            <td>
                {% if row.is_correct %}
                    ✅
                {% else %}
                    ❌
                {% endif %}
            </td>
        </tr>
        {% endfor %}
    </tbody>
</table>

<div class="hero-buttons">
    <a class="btn secondary" href="/quiz">Quiz חדש</a>
    <a class="btn" href="/flashcards">חזרה לכרטיסיות</a>
</div>
"""
)

# ==================== VOCABULARY DATA ====================
WORDS = [
    # REVIEW
    {"id": 1, "english": "every single moment", "hebrew": "כל רגע ורגע"},
    {"id": 2, "english": "excitement (n)", "hebrew": "התרגשות"},

    # PART 1
    {"id": 3, "english": "colleague (n)", "hebrew": "עמית / קולגה"},
    {"id": 4, "english": "favor (n)", "hebrew": "טובה"},
    {"id": 5, "english": "ancient (adj)", "hebrew": "עתיק"},
    {"id": 6, "english": "consider (to be) (v)", "hebrew": "לראות כ / לשקול"},
    {"id": 7, "english": "find (it) (funny)", "hebrew": "למצוא (משהו) מצחיק"},
    {"id": 8, "english": "laugh at", "hebrew": "לצחוק על"},
    {"id": 9, "english": "importance (n)", "hebrew": "חשיבות"},
    {"id": 10, "english": "jar (n)", "hebrew": "צנצנת"},
    {"id": 11, "english": "joke (n)", "hebrew": "בדיחה"},
    {"id": 12, "english": "roll (n, v)", "hebrew": "גלגול / להתגלגל"},
    {"id": 13, "english": "see (v)", "hebrew": "לראות"},
    {"id": 14, "english": "selfie (n)", "hebrew": "סלפי"},
    {"id": 15, "english": "sense of humor", "hebrew": "חוש הומור"},

    # PART 2
    {"id": 16, "english": "adjective (n)", "hebrew": "שם תואר"},
    {"id": 17, "english": "culture (n)", "hebrew": "תרבות"},
    {"id": 18, "english": "dictation (n)", "hebrew": "הכתבה"},
    {"id": 19, "english": "adverb (n)", "hebrew": "תואר הפועל"},
    {"id": 20, "english": "eventually (adv)", "hebrew": "בסופו של דבר"},
    {"id": 21, "english": "pass through", "hebrew": "לעבור דרך"},
    {"id": 22, "english": "arrange (v)", "hebrew": "לסדר / לארגן"},
    {"id": 23, "english": "excuse (n)", "hebrew": "תירוץ"},
    {"id": 24, "english": "article", "hebrew": "מאמר"},
    {"id": 25, "english": "contrast (n, v)", "hebrew": "ניגוד / להשוות בניגוד"},
    {"id": 26, "english": "fire (n, v)", "hebrew": "אש / לפטר / לירות"},
    {"id": 27, "english": "mean (adj)", "hebrew": "מרושע"},
    {"id": 28, "english": "smell (n, v)", "hebrew": "ריח / להריח"},
    {"id": 29, "english": "at all", "hebrew": "בכלל"},
    {"id": 30, "english": "as if", "hebrew": "כאילו"},
    {"id": 31, "english": "cut", "hebrew": "לחתוך"},
    {"id": 32, "english": "for instance", "hebrew": "למשל"},
    {"id": 33, "english": "attach (v)", "hebrew": "לצרף"},
    {"id": 34, "english": "defend (v)", "hebrew": "להגן"},
    {"id": 35, "english": "forgive (v)", "hebrew": "לסלוח"},
    {"id": 36, "english": "midday (n)", "hebrew": "צהריים"},
    {"id": 37, "english": "mind (n, v)", "hebrew": "שכל / אכפת / להתנגד"},
    {"id": 38, "english": "smoke (n, v)", "hebrew": "עשן / לעשן"},
    {"id": 39, "english": "attitude (n)", "hebrew": "גישה"},
    {"id": 40, "english": "gas", "hebrew": "גז / דלק"},
    {"id": 41, "english": "so that", "hebrew": "כדי ש..."},
    {"id": 42, "english": "be expecting", "hebrew": "לצפות (למשהו)"},
    {"id": 43, "english": "in other words", "hebrew": "במילים אחרות"},
    {"id": 44, "english": "attempt (v)", "hebrew": "ניסיון / לנסות"},
    {"id": 45, "english": "deny (v)", "hebrew": "להכחיש"},
    {"id": 46, "english": "gather (v)", "hebrew": "לאסוף / להתאסף"},
    {"id": 47, "english": "nowadays (adv)", "hebrew": "בימינו"},
    {"id": 48, "english": "stranger (n)", "hebrew": "זר"},
    {"id": 49, "english": "base on", "hebrew": "לבסס על"},
    {"id": 50, "english": "dive (v)", "hebrew": "לצלול"},
    {"id": 51, "english": "give (someone) a call", "hebrew": "להתקשר ל..."},
    {"id": 52, "english": "play a trick on", "hebrew": "לעשות תעלול ל..."},
    {"id": 53, "english": "study (n, v)", "hebrew": "לימוד / ללמוד"},
    {"id": 54, "english": "board (v)", "hebrew": "לעלות (למטוס/אוטובוס)"},
    {"id": 55, "english": "just (adv)", "hebrew": "רק / פשוט"},
    {"id": 56, "english": "knock (v)", "hebrew": "לדפוק"},
    {"id": 57, "english": "borrow (v)", "hebrew": "לשאול (לקחת בהשאלה)"},
    {"id": 58, "english": "duty (n)", "hebrew": "חובה / תפקיד"},
    {"id": 59, "english": "happiness (n)", "hebrew": "אושר"},
    {"id": 60, "english": "pop (n)", "hebrew": "פופ / פקיעה קלה"},
    {"id": 61, "english": "the public", "hebrew": "הציבור"},
    {"id": 62, "english": "certain (adj)", "hebrew": "מסוים / בטוח"},
    {"id": 63, "english": "bring (someone) luck", "hebrew": "להביא מזל (למישהו)"},
    {"id": 64, "english": "later (adv)", "hebrew": "אחר כך"},
    {"id": 65, "english": "elementary (adj)", "hebrew": "יסודי"},
    {"id": 66, "english": "hardly (adv)", "hebrew": "בקושי"},
    {"id": 67, "english": "record (n, v)", "hebrew": "שיא / להקליט"},
    {"id": 68, "english": "the same thing", "hebrew": "אותו דבר"},
    {"id": 69, "english": "complex (adj)", "hebrew": "מורכב"},
    {"id": 70, "english": "care (v)", "hebrew": "אכפת / לדאוג"},
    {"id": 71, "english": "lay the table", "hebrew": "לערוך את השולחן"},
    {"id": 72, "english": "elevator (n)", "hebrew": "מעלית"},
    {"id": 73, "english": "hit (n)", "hebrew": "פגיעה / להיט"},
    {"id": 74, "english": "result in", "hebrew": "לגרום ל"},
    {"id": 75, "english": "tweet (n, v)", "hebrew": "ציוץ / לצייץ"},
    {"id": 76, "english": "crucial (adj)", "hebrew": "קריטי"},
    {"id": 77, "english": "period (n)", "hebrew": "תקופה / נקודה"},
    {"id": 78, "english": "experience (n)", "hebrew": "ניסיון / חוויה"},
    {"id": 79, "english": "phrase (n)", "hebrew": "ביטוי / צירוף מילים"},
    {"id": 80, "english": "noun", "hebrew": "שם עצם"},
    {"id": 81, "english": "the press (n)", "hebrew": "העיתונות"},
    {"id": 82, "english": "paragraph (n)", "hebrew": "פסקה"},
    {"id": 83, "english": "to be honest", "hebrew": "בכנות / האמת היא ש..."},
    {"id": 84, "english": "tone (n)", "hebrew": "טון / נימה"},
    {"id": 85, "english": "understanding (n)", "hebrew": "הבנה"},

    # SPEAK YOUR MIND
    {"id": 86, "english": "advantage (n)", "hebrew": "יתרון"},
    {"id": 87, "english": "disadvantage (n)", "hebrew": "חיסרון"},
    {"id": 88, "english": "express (v)", "hebrew": "לבטא"},
    {"id": 89, "english": "in detail", "hebrew": "בפירוט"},
    {"id": 90, "english": "plural (n, adj)", "hebrew": "רבים"},
    {"id": 91, "english": "in fact", "hebrew": "למעשה"},
    {"id": 92, "english": "question mark (n)", "hebrew": "סימן שאלה"},
    {"id": 93, "english": "rather (adv)", "hebrew": "די / עדיף / במקום"},
    {"id": 94, "english": "relatively (adv)", "hebrew": "יחסית"},
    {"id": 95, "english": "route (n)", "hebrew": "מסלול / דרך"},
    {"id": 96, "english": "singular (adj)", "hebrew": "יחיד"},
    {"id": 97, "english": "noticeboard (n)", "hebrew": "לוח מודעות"},
    {"id": 98, "english": "tense (n)", "hebrew": "זמן (דקדוקי)"},
    {"id": 99, "english": "notes (n)", "hebrew": "הערות / סיכומים"},
    {"id": 100, "english": "opinion (n)", "hebrew": "דעה"},
    {"id": 101, "english": "speaker (n)", "hebrew": "דובר"},
    {"id": 102, "english": "speech (n)", "hebrew": "נאום"},
    {"id": 103, "english": "support (v)", "hebrew": "לתמוך"},
    {"id": 104, "english": "topic (n)", "hebrew": "נושא"},
]


# ==================== ROUTES ====================
@app.route("/")
def index():
    """Home page - choose between flashcards or quiz"""
    return render_template_string(INDEX_TEMPLATE, total=len(WORDS), css=CSS_STYLES)


@app.route("/flashcards")
def flashcards():
    """Display flashcards - English on one side, Hebrew on the other"""
    return render_template_string(FLASHCARDS_TEMPLATE, words=WORDS, css=CSS_STYLES)


@app.route("/quiz", methods=["GET", "POST"])
def quiz():
    """
    GET - Create new quiz with 20 random words
    POST - Check answers and display results
    """
    if request.method == "GET":
        # Take up to 20 random words
        questions = random.sample(WORDS, min(50, len(WORDS)))

        quiz_data = []
        for word in questions:
            # Three random wrong answers
            wrong = random.sample(
                [w for w in WORDS if w["id"] != word["id"]],
                3
            )
            options = [word["hebrew"]] + [w["hebrew"] for w in wrong]
            random.shuffle(options)

            quiz_data.append({
                "id": word["id"],
                "english": word["english"],
                "options": options
            })

        # Save correct answers in session
        session["quiz_answers"] = {str(w["id"]): w["hebrew"] for w in questions}

        return render_template_string(QUIZ_TEMPLATE, questions=quiz_data, css=CSS_STYLES)

    # POST - Check answers
    answers = session.get("quiz_answers", {})
    total = len(answers)
    correct_count = 0
    details = []

    for word_id, correct_hebrew in answers.items():
        chosen = request.form.get(word_id)
        is_correct = (chosen == correct_hebrew)
        if is_correct:
            correct_count += 1

        english_word = next(
            (w["english"] for w in WORDS if w["id"] == int(word_id)),
            "UNKNOWN"
        )

        details.append({
            "english": english_word,
            "correct_hebrew": correct_hebrew,
            "chosen_hebrew": chosen or "—",
            "is_correct": is_correct
        })

    score = int(correct_count / total * 100) if total > 0 else 0

    return render_template_string(
        QUIZ_RESULT_TEMPLATE,
        correct=correct_count,
        total=total,
        score=score,
        details=details,
        css=CSS_STYLES
    )


if __name__ == "__main__":
    print("=" * 60)
    print("🚀 Starting Vocabulary Trainer Flask App...")
    print("=" * 60)
    print("📚 Total words in database:", len(WORDS))
    print("🌐 Server starting at: http://127.0.0.1:5000")
    print("🌐 Also accessible at: http://localhost:5000")
    print("=" * 60)
    print("Press CTRL+C to stop the server")
    print("=" * 60)
    app.run(debug=True, host='0.0.0.0', port=5000)
