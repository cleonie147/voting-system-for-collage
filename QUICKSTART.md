# Quick Start Guide

Choose your preferred method to run the College Voting System:

## 🖥️ Desktop App (Recommended)

**Windows - Double Click:**
- `run_desktop_app.bat`

**PowerShell:**
```powershell
.\run_desktop_app.ps1
```

Opens in app mode (looks like a native app, not a browser).

---

## 🌐 Web Browser Mode

**Setup:**
```powershell
python -m venv .venv
.\.venv\Scripts\pip.exe install -r requirements.txt
```

**Run:**
```powershell
.\.venv\Scripts\python.exe app.py
```

Then open: http://127.0.0.1:5000

---

## 📝 First Time Use

### 1. Register a Student Account
- Go to registration page
- Fill in:
  - Full Name
  - **Gmail Address** (must end with @gmail.com)
  - College ID
  - Password
- Click "Create Account"

### 2. Login and Vote
- Login with your College ID and password
- See all candidates with their photos and branches
- Click on a candidate card to select
- Click "Submit My Vote"

### 3. Admin Access
Login with:
- **College ID:** `admin`
- **Password:** `admin123`

View:
- Total votes
- Results with percentages
- Progress bars
- Candidate photos and branches

---

## 🎨 Features

✅ **Gmail Validation** - Only @gmail.com addresses accepted  
✅ **Progress Bars** - Visual vote percentages  
✅ **Desktop App** - Runs like native Windows app  
✅ **Modern UI** - Colorful, gradient design  
✅ **Candidate Photos** - Shows photo and branch  
✅ **Real-time Results** - Admin dashboard updates live  

---

## ❗ Troubleshooting

**"Email must be a valid Gmail address"**
→ Use an email ending with @gmail.com

**Port 5000 already in use**
→ Stop other apps using port 5000 or change port in app.py

**Database errors**
→ Delete `database/app.db` and restart (auto-recreates)

---

## 📚 More Info

- Full documentation: `README.md`
- Desktop app guide: `DESKTOP_APP.md`
- Recent changes: `CHANGELOG.md`
- For developers: `WARP.md`
