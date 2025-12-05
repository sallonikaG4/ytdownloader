#!/usr/bin/env python3
"""
Desktop Application Wrapper for YouTube to MP3 Downloader
Uses PyQt5 WebEngine to display the Flask app in a native window
"""

import sys
import os
import threading
import time
import webbrowser
from pathlib import Path

# Check if PyQt5 is available
try:
    from PyQt5.QtCore import QUrl, Qt, QTimer, QSettings
    from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QHBoxLayout, QFileDialog, QMessageBox
    from PyQt5.QtWebEngineWidgets import QWebEngineView
    from PyQt5.QtGui import QIcon
except ImportError:
    print("ERROR: PyQt5 is required but not installed.")
    print("Please install it with: pip install PyQt5 PyQtWebEngine")
    sys.exit(1)

# Import Flask app
from app import app as flask_app


class YouTubeDownloaderApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.server_thread = None
        self.downloads_folder = None
        self.settings = QSettings("WaLLe", "YouTubeToMP3")
        self.select_downloads_folder()
        self.init_ui()
        self.start_flask_server()
        
    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle("YouTube to MP3 Downloader")
        self.setGeometry(100, 100, 1200, 800)
        
        # Set window icon if available
        icon_path = self.get_icon_path()
        if icon_path and os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Create layout
        layout = QVBoxLayout()
        central_widget.setLayout(layout)
        
        # Exit button is handled in the web UI (top-right corner)
        # No separate toolbar needed
        
        # Create web view
        self.web_view = QWebEngineView()
        self.web_view.setStyleSheet("background-color: #0f172a;")
        layout.addWidget(self.web_view)
        
        # Wait a bit for server to start, then load the page
        QTimer.singleShot(1000, self.load_app)
        
    def select_downloads_folder(self):
        """Show folder selection dialog on startup"""
        # Load saved folder from settings
        saved_folder = self.settings.value("downloads_folder", "")
        
        if saved_folder and os.path.exists(saved_folder):
            self.downloads_folder = saved_folder
            return
        
        # Show folder selection dialog
        from youtube_downloader import get_default_downloads_dir
        default_folder = str(get_default_downloads_dir())
        
        folder = QFileDialog.getExistingDirectory(
            self,
            "Select Downloads Folder",
            default_folder,
            QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks
        )
        
        if folder:
            self.downloads_folder = folder
            self.settings.setValue("downloads_folder", folder)
        else:
            # Use default if user cancels
            self.downloads_folder = default_folder
            self.settings.setValue("downloads_folder", self.downloads_folder)
    
    def get_icon_path(self):
        """Get the path to the application icon"""
        # Check multiple possible locations
        if getattr(sys, 'frozen', False):
            # Running in a bundle (PyInstaller)
            base_path = Path(sys.executable).parent
        else:
            base_path = Path(__file__).parent
            
        possible_paths = [
            base_path / "icon.ico",
            base_path / "assets" / "icon.ico",
            base_path / "resources" / "icon.ico",
        ]
        
        for path in possible_paths:
            if path.exists():
                return str(path)
        return None
        
    def start_flask_server(self):
        """Start Flask server in a separate thread"""
        def run_server():
            flask_app.run(host='127.0.0.1', port=5000, debug=False, use_reloader=False)
        
        self.server_thread = threading.Thread(target=run_server, daemon=True)
        self.server_thread.start()
        
        # Wait for server to be ready
        max_wait = 10
        waited = 0
        while waited < max_wait:
            try:
                import urllib.request
                urllib.request.urlopen('http://127.0.0.1:5000', timeout=1)
                break
            except:
                time.sleep(0.5)
                waited += 0.5
        
    def load_app(self):
        """Load the Flask app in the web view"""
        # Pass downloads folder to the web app via URL parameter
        if self.downloads_folder:
            url = QUrl(f"http://127.0.0.1:5000?downloads_folder={self.downloads_folder}")
        else:
            url = QUrl("http://127.0.0.1:5000")
        self.web_view.setUrl(url)
        
        # Handle window close requests from JavaScript
        # The web page can call window.close() which will be handled by the WebView
        
    def close_application(self):
        """Close the application"""
        self.close()
        
    def closeEvent(self, event):
        """Handle window close event"""
        # Flask server will stop automatically when thread dies
        event.accept()


def main():
    """Main entry point"""
    # Enable high DPI scaling
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    
    app = QApplication(sys.argv)
    app.setApplicationName("YouTube to MP3 Downloader")
    app.setOrganizationName("Tech Solutions")
    
    # Set application style
    app.setStyle('Fusion')
    
    # Create and show main window
    window = YouTubeDownloaderApp()
    window.show()
    
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

