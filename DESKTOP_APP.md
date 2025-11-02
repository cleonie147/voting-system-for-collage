# College Voting System - Desktop Application

This guide explains how to run the voting system as a desktop application.

## Quick Start

### Windows

**Option 1: Using Batch File (Easiest)**
Simply double-click `run_desktop_app.bat`

**Option 2: Using PowerShell**
Right-click `run_desktop_app.ps1` → Run with PowerShell

**Option 3: Manual**
```powershell
.\.venv\Scripts\python.exe app_desktop.py
```

## Features

- **App Mode**: Opens in Chrome/Edge app mode (no browser UI) for a native feel
- **Auto-Start**: Automatically starts the Flask server and opens the browser
- **Clean Exit**: Press Ctrl+C to stop the server

## How It Works

The desktop launcher (`app_desktop.py`):
1. Starts Flask server on port 5000 in the background
2. Waits 2 seconds for server to initialize
3. Opens the app in your browser:
   - First tries Chrome in `--app` mode (frameless window)
   - Then tries Edge in `--app` mode
   - Falls back to default browser if neither is available

## App Mode Benefits

When running in Chrome/Edge app mode:
- No address bar or browser tabs
- Looks like a native desktop application
- Dedicated window icon
- Can be pinned to taskbar

## Creating a Desktop Shortcut

1. Right-click `run_desktop_app.bat`
2. Select "Create shortcut"
3. Right-click the shortcut → Properties
4. Click "Change Icon" to customize (optional)
5. Move shortcut to Desktop or Start Menu

## Building a Standalone Executable (Optional)

To create a single `.exe` file:

```powershell
# Install PyInstaller
.\.venv\Scripts\pip.exe install pyinstaller

# Create executable
.\.venv\Scripts\pyinstaller.exe --onefile --windowed --name "VotingSystem" --icon=icon.ico app_desktop.py
```

The executable will be in the `dist` folder.

## Troubleshooting

**Port 5000 already in use:**
- Close other applications using port 5000
- Or modify `app_desktop.py` to use a different port

**Browser doesn't open:**
- Manually navigate to http://127.0.0.1:5000
- Check firewall settings

**Database errors:**
- Delete `database/app.db` and restart
- The database will be recreated automatically
