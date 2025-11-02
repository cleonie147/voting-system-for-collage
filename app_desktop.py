"""
College Voting System - Desktop Application Launcher
Runs Flask backend and opens in browser with app-like experience
"""

import webbrowser
import threading
import time
import sys
import os
from app import app

def run_flask():
    """Run Flask app"""
    app.run(debug=False, port=5000, use_reloader=False)

def open_browser():
    """Open browser after Flask starts"""
    time.sleep(2)  # Wait for Flask to start
    
    # Open in app mode (no browser UI) if Chrome/Edge is available
    url = 'http://127.0.0.1:5000'
    
    # Try Chrome app mode first (cleanest look)
    chrome_paths = [
        r'C:\Program Files\Google\Chrome\Application\chrome.exe',
        r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe',
        os.path.expandvars(r'%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe')
    ]
    
    for chrome_path in chrome_paths:
        if os.path.exists(chrome_path):
            os.system(f'start "" "{chrome_path}" --app="{url}" --window-size=1200,800')
            return
    
    # Try Edge app mode (built into Windows 10/11)
    edge_path = r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'
    if os.path.exists(edge_path):
        os.system(f'start "" "{edge_path}" --app="{url}" --window-size=1200,800')
        return
    
    # Fallback to default browser
    webbrowser.open(url)

def main():
    """Main function to launch the app"""
    print("="*60)
    print("  College Voting System - Desktop App")
    print("="*60)
    print("\nStarting server...")
    print("\nThe application will open in your browser.")
    print("\nTo stop the server, close this window or press Ctrl+C")
    print("="*60)
    print()
    
    # Start Flask in a separate thread
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()
    
    # Open browser in a separate thread
    browser_thread = threading.Thread(target=open_browser, daemon=True)
    browser_thread.start()
    
    # Keep the main thread alive
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\nShutting down...")
        sys.exit(0)

if __name__ == '__main__':
    main()
