# Changelog - College Voting System

## Recent Updates

### ✅ Email Validation with Gmail Requirement
- **Added email field** to user registration
- **Gmail validation**: Only @gmail.com addresses are accepted
- **Visual feedback**: Error message appears if non-Gmail address is entered
- **HTML5 validation**: Client-side pattern matching for immediate feedback
- **Server-side validation**: Double-checks email format on backend

### ✅ Fixed Progress Bar Visualization
- **Dynamic width**: Progress bars now correctly fill according to vote percentage
- **Percentage display**: Shows exact percentage inside the progress bar
- **Sorted results**: Candidates are sorted by vote count (highest first)
- **Color gradient**: Beautiful purple gradient for progress bars

### ✅ Desktop Application Support
- **App Mode**: Launches in Chrome/Edge app mode (frameless window)
- **Auto-start**: Flask server starts automatically
- **One-click launch**: Use `run_desktop_app.bat` or `run_desktop_app.ps1`
- **Native feel**: Looks like a desktop application, not a website

### Previous Features

#### Modern UI/UX
- **Colorful gradient design**: Purple/blue gradient background
- **Candidate cards**: Large circular photos with hover effects
- **Branch display**: Shows each candidate's engineering branch
- **Bootstrap Icons**: Professional icons throughout
- **Responsive layout**: Works on desktop, tablet, and mobile

#### Admin Dashboard
- **Live statistics**: Total votes, candidate count, participation rate
- **Visual results**: Photo, name, branch, and vote count for each candidate
- **Progress bars**: Visual representation of vote percentages
- **Sorted leaderboard**: Candidates ordered by votes received

#### Security
- **Password hashing**: Werkzeug PBKDF2 encryption
- **Session management**: Secure Flask sessions
- **Vote integrity**: Multiple safeguards prevent duplicate voting
- **Email uniqueness**: Each email can only register once

## Database Schema Updates

### Users Table
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    college_id TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,  -- NEW FIELD
    password_hash TEXT NOT NULL,
    is_admin INTEGER NOT NULL DEFAULT 0
);
```

### Candidates Table
```sql
CREATE TABLE candidates (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,
    branch TEXT NOT NULL,        -- NEW FIELD
    photo_url TEXT NOT NULL      -- NEW FIELD
);
```

## File Structure

```
college-voting-system/
├── app.py                      # Main Flask application
├── app_desktop.py             # Desktop launcher (NEW)
├── run_desktop_app.bat        # Windows batch launcher (NEW)
├── run_desktop_app.ps1        # PowerShell launcher (NEW)
├── requirements.txt           # Python dependencies
├── README.md                  # Main documentation
├── DESKTOP_APP.md            # Desktop app guide (NEW)
├── CHANGELOG.md              # This file (NEW)
├── WARP.md                   # Warp AI guidance
├── database/
│   ├── app.db                # SQLite database (auto-generated)
│   └── schema.sql            # Reference schema
├── templates/
│   ├── base.html             # Updated with Bootstrap Icons
│   ├── login.html            # Modernized design
│   ├── register.html         # Added email field (UPDATED)
│   ├── vote.html             # Card-based layout (UPDATED)
│   ├── confirmation.html     # Success animation
│   └── admin.html            # Dashboard with progress bars (UPDATED)
└── static/
    ├── css/
    │   └── styles.css        # Colorful modern design (UPDATED)
    └── js/
        └── app.js            # Client-side scripts
```

## How to Use New Features

### Email Validation
1. Go to registration page
2. Enter email address
3. If it doesn't end with `@gmail.com`, you'll see an error:
   - Red error message: "Email must be a valid Gmail address (@gmail.com)."
   - HTML5 validation also prevents form submission

### Desktop App
1. **Windows**: Double-click `run_desktop_app.bat`
2. **PowerShell**: Run `.\run_desktop_app.ps1`
3. **Manual**: `.\.venv\Scripts\python.exe app_desktop.py`

### View Progress Bars
1. Login as admin (college_id: `admin`, password: `admin123`)
2. Navigate to Dashboard
3. See live voting results with:
   - Vote counts
   - Percentage bars
   - Candidate photos and branches

## Breaking Changes

⚠️ **Database Reset Required**
- The email field is now required
- Old databases must be deleted and recreated
- Delete `database/app.db` to trigger automatic recreation

## Next Steps

Potential future enhancements:
- [ ] Real-time vote updates via WebSockets
- [ ] Vote analytics and charts
- [ ] Candidate profile pages
- [ ] Email notifications
- [ ] Multi-language support
- [ ] Dark mode toggle
