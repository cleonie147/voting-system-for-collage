# College Voting System (Flask + SQLite)

A complete web-based college voting system built with Flask (Python), SQLite, HTML, CSS, JavaScript, and Bootstrap.

## Features
- Student login and authentication (college ID + password)
- Password hashing (secure login)
- Each student can vote only once (DB constraint + logic)
- SQLite database for users, candidates, and votes
- Admin dashboard to view total votes and results per candidate
- Confirmation page after voting
- Duplicate vote prevention
- Logout, error handling, and success messages

## Project structure
```
college-voting-system/
├── app.py
├── requirements.txt
├── .gitignore
├── README.md
├── database/
│   └── schema.sql
├── templates/
│   ├── base.html
│   ├── login.html
│   ├── register.html
│   ├── vote.html
│   ├── confirmation.html
│   └── admin.html
└── static/
    ├── css/
    │   └── styles.css
    └── js/
        └── app.js
```

## Prerequisites
- Python 3.9+ (Windows/Linux)
- pip
- (Optional) Git

## Setup (Windows PowerShell)
```
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```
Then open http://127.0.0.1:5000/ in your browser.

## Setup (Linux/macOS)
```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```
Then open http://127.0.0.1:5000/ in your browser.

## Default data
- Admin login: college ID `admin`, password `admin123`
- Sample candidates are seeded on first run (Alice, Bob, Charlie)
- Students should self-register once with their college ID

## Notes
- The database file will be created at `database/app.db` on first run.
- If Git is not installed, you can install it later and run `git init` from the project directory.
- For production use, configure a strong `SECRET_KEY` environment variable.
