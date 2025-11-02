from flask import Flask, render_template, request, redirect, url_for, session, flash, g
import os
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, 'database', 'app.db')

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-change-me')

# --- Database helpers ---

def get_db():
    if 'db' not in g:
        os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
        g.db = sqlite3.connect(DB_PATH)
        g.db.row_factory = sqlite3.Row
    return g.db

@app.teardown_appcontext
def close_db(error=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()


def init_db():
    db = get_db()
    db.executescript(
        '''
        PRAGMA foreign_keys = ON;

        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            college_id TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            is_admin INTEGER NOT NULL DEFAULT 0
        );

        CREATE TABLE IF NOT EXISTS candidates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            branch TEXT NOT NULL,
            photo_url TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS votes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            candidate_id INTEGER NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(student_id),
            FOREIGN KEY(student_id) REFERENCES users(id) ON DELETE CASCADE,
            FOREIGN KEY(candidate_id) REFERENCES candidates(id) ON DELETE CASCADE
        );
        '''
    )

    # Seed candidates if empty
    cnt = db.execute('SELECT COUNT(*) AS c FROM candidates').fetchone()['c']
    if cnt == 0:
        db.executemany('INSERT INTO candidates(name, branch, photo_url) VALUES (?, ?, ?)', [
            ('Rahul Sharma', 'Computer Science', 'https://randomuser.me/api/portraits/men/32.jpg'),
            ('Priya Patel', 'Electrical Engineering', 'https://randomuser.me/api/portraits/women/44.jpg'),
            ('Arjun Singh', 'Mechanical Engineering', 'https://randomuser.me/api/portraits/men/54.jpg'),
            ('Sneha Reddy', 'Information Technology', 'https://randomuser.me/api/portraits/women/68.jpg'),
            ('Vikram Kumar', 'Civil Engineering', 'https://randomuser.me/api/portraits/men/22.jpg'),
        ])

    # Seed admin user if not exists
    admin = db.execute('SELECT id FROM users WHERE college_id = ?', ('admin',)).fetchone()
    if not admin:
        db.execute(
            'INSERT INTO users(college_id, name, email, password_hash, is_admin) VALUES (?, ?, ?, ?, 1)',
            ('admin', 'Administrator', 'admin@college.edu', generate_password_hash('admin123'))
        )

    db.commit()


def ensure_db():
    # Create file if it does not exist, then init schema/seed
    if not os.path.exists(DB_PATH):
        os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
        open(DB_PATH, 'a').close()
    init_db()


# --- Auth helpers ---

def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to continue.', 'warning')
            return redirect(url_for('login'))
        return view(*args, **kwargs)
    return wrapped


def admin_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to continue.', 'warning')
            return redirect(url_for('login'))
        if not session.get('is_admin'):
            flash('Admin access required.', 'danger')
            return redirect(url_for('index'))
        return view(*args, **kwargs)
    return wrapped


@app.before_request
def _before():
    ensure_db()


# --- Routes ---
@app.route('/')
def index():
    if 'user_id' in session:
        if session.get('is_admin'):
            return redirect(url_for('admin'))
        return redirect(url_for('vote'))
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip().lower()
        college_id = request.form.get('college_id', '').strip()
        password = request.form.get('password', '')

        if not name or not email or not college_id or not password:
            flash('All fields are required.', 'warning')
            return render_template('register.html')

        # Validate email has @ symbol
        if '@' not in email or email.count('@') != 1:
            flash('Please enter a valid email address.', 'danger')
            return render_template('register.html')

        db = get_db()
        existing = db.execute('SELECT id FROM users WHERE college_id = ?', (college_id,)).fetchone()
        if existing:
            flash('This college ID is already registered. Please log in.', 'warning')
            return redirect(url_for('login'))

        existing_email = db.execute('SELECT id FROM users WHERE email = ?', (email,)).fetchone()
        if existing_email:
            flash('This email is already registered. Please log in.', 'warning')
            return redirect(url_for('login'))

        db.execute(
            'INSERT INTO users (college_id, name, email, password_hash, is_admin) VALUES (?, ?, ?, ?, 0)',
            (college_id, name, email, generate_password_hash(password))
        )
        db.commit()
        flash('Registration successful. Please log in.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        college_id = request.form.get('college_id', '').strip()
        password = request.form.get('password', '')

        db = get_db()
        user = db.execute('SELECT * FROM users WHERE college_id = ?', (college_id,)).fetchone()
        if not user or not check_password_hash(user['password_hash'], password):
            flash('Invalid credentials.', 'danger')
            return render_template('login.html')

        session.clear()
        session['user_id'] = user['id']
        session['college_id'] = user['college_id']
        session['name'] = user['name']
        session['is_admin'] = bool(user['is_admin'])
        flash('Logged in successfully.', 'success')
        return redirect(url_for('index'))

    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    session.clear()
    flash('Logged out.', 'info')
    return redirect(url_for('login'))


@app.route('/vote', methods=['GET', 'POST'])
@login_required
def vote():
    if session.get('is_admin'):
        return redirect(url_for('admin'))

    db = get_db()
    user_id = session['user_id']

    # Check if user has already voted
    existing_vote = db.execute('SELECT * FROM votes WHERE student_id = ?', (user_id,)).fetchone()
    if existing_vote:
        flash('You have already voted.', 'info')
        return redirect(url_for('confirmation'))

    candidates = db.execute('SELECT * FROM candidates ORDER BY name').fetchall()

    if request.method == 'POST':
        candidate_id = request.form.get('candidate_id')
        if not candidate_id:
            flash('Please select a candidate.', 'warning')
            return render_template('vote.html', candidates=candidates)
        try:
            db.execute('INSERT INTO votes (student_id, candidate_id) VALUES (?, ?)', (user_id, candidate_id))
            db.commit()
        except sqlite3.IntegrityError:
            flash('You have already voted.', 'info')
            return redirect(url_for('confirmation'))
        flash('Vote submitted successfully!', 'success')
        return redirect(url_for('confirmation'))

    return render_template('vote.html', candidates=candidates)


@app.route('/confirmation')
@login_required
def confirmation():
    db = get_db()
    user_id = session['user_id']
    row = db.execute(
        'SELECT c.name AS candidate_name, v.created_at FROM votes v JOIN candidates c ON v.candidate_id = c.id WHERE v.student_id = ?',
        (user_id,)
    ).fetchone()
    if not row:
        flash('No vote found. Please vote first.', 'warning')
        return redirect(url_for('vote'))
    return render_template('confirmation.html', candidate_name=row['candidate_name'], voted_at=row['created_at'])


@app.route('/admin')
@admin_required
def admin():
    db = get_db()
    total_votes = db.execute('SELECT COUNT(*) AS c FROM votes').fetchone()['c']
    results = db.execute(
        'SELECT c.name AS candidate, c.branch, c.photo_url, COUNT(v.id) AS count '\
        'FROM candidates c LEFT JOIN votes v ON v.candidate_id = c.id '\
        'GROUP BY c.id ORDER BY count DESC, c.name'
    ).fetchall()
    return render_template('admin.html', total_votes=total_votes, results=results)


if __name__ == '__main__':
    # Dev server
    app.run(debug=True)
