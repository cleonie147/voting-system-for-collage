# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Commands

### Setup and Environment
```powershell
# Windows PowerShell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

```bash
# Linux/macOS
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Running the Application
```bash
python app.py
```
The dev server starts at http://127.0.0.1:5000/ with debug mode enabled.

### Database Management
The database is automatically initialized on first run. To reset:
```powershell
# Windows
Remove-Item -Path database\app.db -Force
python app.py  # Will recreate database with seed data
```

```bash
# Linux/macOS
rm database/app.db
python app.py  # Will recreate database with seed data
```

## Architecture Overview

### Application Structure
This is a Flask-based monolithic web application using SQLite for persistence. The entire backend logic resides in `app.py` (~250 lines), making it a simple single-file application.

### Database Architecture
The database uses SQLite with three core tables enforcing referential integrity:

- **users**: Stores student accounts and admin accounts with hashed passwords (using Werkzeug's PBKDF2)
- **candidates**: Stores candidates available for voting
- **votes**: Junction table linking students to candidates with a UNIQUE constraint on `student_id` to enforce one-vote-per-student at the database level

Foreign keys are enabled (`PRAGMA foreign_keys = ON`) and cascade deletes are configured. The schema is defined inline in `app.py:init_db()`, not from the reference `database/schema.sql` file.

### Session and Authentication Flow
- Flask sessions store user state (user_id, college_id, name, is_admin)
- Two decorators enforce access control:
  - `@login_required`: Protects student routes (vote, confirmation, logout)
  - `@admin_required`: Protects admin dashboard
- Password hashing uses `werkzeug.security.generate_password_hash` and `check_password_hash`
- The `SECRET_KEY` defaults to 'dev-secret-change-me' unless overridden via environment variable

### Request Lifecycle
1. `@app.before_request` ensures database exists and is initialized before every request
2. `get_db()` stores the database connection in Flask's `g` object for request-scoped access
3. `@app.teardown_appcontext` closes the database connection after each request

### Vote Integrity System
Vote uniqueness is enforced at multiple levels:
- Database: UNIQUE constraint on `votes.student_id`
- Application: Check for existing vote before rendering vote form
- Transaction: sqlite3.IntegrityError catch on duplicate vote attempt

### Frontend Stack
- **Templates**: Jinja2 templates with Bootstrap 5.3.3 (CDN)
- **Base template**: `templates/base.html` provides navbar, flash message handling, and layout
- **Static assets**: Minimal custom CSS/JS in `static/` directory

## Development Guidelines

### Modifying Database Schema
Schema changes must be made in `app.py:init_db()` function, not in `database/schema.sql` (which is only a reference). After schema changes, delete `database/app.db` to trigger re-initialization.

### Adding New Routes
- Use `@login_required` for student-only routes
- Use `@admin_required` for admin-only routes
- Access database via `get_db()` - never create direct connections
- Always call `db.commit()` after write operations

### Security Considerations
- Never store plain-text passwords - use `generate_password_hash()` for new users
- Set `SECRET_KEY` environment variable for production deployments
- Session data is stored client-side in signed cookies - sensitive data should not be added to session

### Default Credentials
- Admin: college_id=`admin`, password=`admin123`
- Default candidates: Alice, Bob, Charlie (seeded automatically)

### Testing Voting Flow
1. Register a new student account (any college_id except 'admin')
2. Login with that account
3. Submit a vote for a candidate
4. Verify duplicate vote prevention (refresh /vote should redirect to confirmation)
5. Login as admin to view results at /admin
