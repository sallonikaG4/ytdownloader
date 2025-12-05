#!/usr/bin/env python3
"""
Flask Web Application for YouTube to MP3 Downloader
Modern, tech-savvy UI for downloading YouTube videos and playlists
"""

from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import sys
import json
from pathlib import Path
from youtube_downloader import YouTubeDownloader
import threading
import time

# Handle PyInstaller bundle
if getattr(sys, 'frozen', False):
    # Running in a bundle (PyInstaller)
    template_folder = os.path.join(sys._MEIPASS, 'templates')
    static_folder = os.path.join(sys._MEIPASS, 'static')
    app = Flask(__name__, template_folder=template_folder, static_folder=static_folder)
else:
    # Running in a normal Python environment
    app = Flask(__name__)

CORS(app)

# Global download state
download_state = {
    'active': False,
    'progress': 0,
    'status': 'idle',
    'current_item': '',
    'total_items': 0,
    'current_item_num': 0,
    'speed': 0,
    'eta': 0,
    'error': None
}

download_lock = threading.Lock()


def progress_callback(data):
    """Callback for download progress updates"""
    global download_state
    with download_lock:
        if data.get('status') == 'downloading':
            download_state['progress'] = data.get('percent', 0)
            download_state['status'] = 'downloading'
            download_state['speed'] = data.get('speed', 0)
            download_state['eta'] = data.get('eta', 0)
        elif data.get('status') == 'converting':
            download_state['status'] = 'converting'
            download_state['progress'] = 100


# Global variable to store selected downloads folder
selected_downloads_folder = None

@app.route('/')
def index():
    """Main page"""
    global selected_downloads_folder
    
    # Get downloads folder from query parameter (set by desktop app)
    downloads_folder = request.args.get('downloads_folder')
    if downloads_folder:
        selected_downloads_folder = downloads_folder
        default_path = downloads_folder
    else:
        from youtube_downloader import get_default_downloads_dir
        default_path = str(get_default_downloads_dir())
        if selected_downloads_folder is None:
            selected_downloads_folder = default_path
    
    return render_template('index.html', default_downloads_path=default_path)


@app.route('/api/info', methods=['POST'])
def get_info():
    """Get video/playlist information"""
    try:
        data = request.json
        url = data.get('url', '').strip()
        
        if not url:
            return jsonify({'error': 'URL is required'}), 400
        
        try:
            # Use default downloads directory (user-writable)
            downloader = YouTubeDownloader()
            info = downloader.get_video_info(url)
            
            # Include default downloads path in response
            from youtube_downloader import get_default_downloads_dir
            default_path = str(get_default_downloads_dir())
            
            return jsonify({
                'success': True, 
                'info': info,
                'default_downloads_path': default_path
            })
        except Exception as e:
            error_msg = str(e)
            # Check if it's an FFmpeg error
            if 'ffmpeg' in error_msg.lower() or 'ffprobe' in error_msg.lower():
                return jsonify({
                    'error': error_msg,
                    'ffmpeg_error': True
                }), 500
            raise
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/download', methods=['POST'])
def download():
    """Start download process"""
    global download_state
    
    try:
        data = request.json
        url = data.get('url', '').strip()
        bitrate = data.get('bitrate', '172k')
        output_dir = data.get('output_dir', None)  # None will use default (user-writable location)
        selected_indices = data.get('selected_indices', None)  # List of selected playlist indices
        
        if not url:
            return jsonify({'error': 'URL is required'}), 400
        
        # Check if download is already in progress
        with download_lock:
            if download_state['active']:
                return jsonify({'error': 'Download already in progress'}), 400
            
            download_state['active'] = True
            download_state['progress'] = 0
            download_state['status'] = 'starting'
            download_state['error'] = None
            download_state['current_item'] = ''
            download_state['total_items'] = 0
            download_state['current_item_num'] = 0
        
        # Start download in background thread
        def download_thread():
            global download_state, selected_downloads_folder
            try:
                # Use selected folder or provided output_dir
                if output_dir is None or output_dir == 'downloads':
                    if selected_downloads_folder:
                        actual_output_dir = selected_downloads_folder
                    else:
                        from youtube_downloader import get_default_downloads_dir
                        actual_output_dir = str(get_default_downloads_dir())
                else:
                    actual_output_dir = output_dir
                
                downloader = YouTubeDownloader(
                    output_dir=actual_output_dir,
                    bitrate=bitrate
                )
                downloader.set_progress_callback(progress_callback)
                
                # Get info first
                info = downloader.get_video_info(url)
                
                # Determine total items count
                if selected_indices and info.get('type') == 'playlist':
                    total_count = len(selected_indices)
                else:
                    total_count = info.get('count', 1)
                
                with download_lock:
                    download_state['total_items'] = total_count
                    download_state['current_item'] = info.get('title', 'Unknown')
                
                # Download with selected indices if provided
                result = downloader.download(
                    url, 
                    progress_callback=progress_callback,
                    selected_indices=selected_indices
                )
                
                with download_lock:
                    download_state['active'] = False
                    download_state['status'] = 'idle'  # Changed to 'idle' to stop polling loop
                    download_state['progress'] = 0
                    download_state['current_item'] = ''
                    download_state['total_items'] = 0
                    download_state['speed'] = 0
                    download_state['eta'] = 0
                    
            except Exception as e:
                with download_lock:
                    download_state['active'] = False
                    download_state['status'] = 'error'
                    download_state['error'] = str(e)
        
        thread = threading.Thread(target=download_thread, daemon=True)
        thread.start()
        
        return jsonify({'success': True, 'message': 'Download started'})
        
    except Exception as e:
        with download_lock:
            download_state['active'] = False
            download_state['status'] = 'error'
            download_state['error'] = str(e)
        return jsonify({'error': str(e)}), 500


@app.route('/api/status', methods=['GET'])
def get_status():
    """Get current download status"""
    global download_state
    with download_lock:
        return jsonify(download_state.copy())


@app.route('/api/downloads', methods=['GET'])
def list_downloads():
    """List downloaded files"""
    try:
        global selected_downloads_folder
        
        output_dir = request.args.get('dir', None)
        if output_dir is None or output_dir == 'downloads':
            if selected_downloads_folder:
                download_path = Path(selected_downloads_folder)
            else:
                from youtube_downloader import get_default_downloads_dir
                download_path = get_default_downloads_dir()
        else:
            download_path = Path(output_dir)
        
        if not download_path.exists():
            return jsonify({'files': [], 'path': str(download_path)})
        
        files = []
        for item in download_path.rglob('*.mp3'):
            files.append({
                'name': item.name,
                'path': str(item.relative_to(download_path)),
                'size': item.stat().st_size,
                'modified': item.stat().st_mtime
            })
        
        # Sort by modified time (newest first)
        files.sort(key=lambda x: x['modified'], reverse=True)
        
        return jsonify({'files': files, 'path': str(download_path)})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/download-file', methods=['GET'])
def download_file():
    """Download a file"""
    try:
        global selected_downloads_folder
        
        file_path = request.args.get('path', '')
        output_dir = request.args.get('dir', None)
        
        if not file_path:
            return jsonify({'error': 'File path is required'}), 400
        
        if output_dir is None or output_dir == 'downloads':
            if selected_downloads_folder:
                download_path = Path(selected_downloads_folder)
            else:
                from youtube_downloader import get_default_downloads_dir
                download_path = get_default_downloads_dir()
        else:
            download_path = Path(output_dir)
        file_full_path = download_path / file_path
        
        if not file_full_path.exists() or not file_full_path.is_file():
            return jsonify({'error': 'File not found'}), 404
        
        return send_from_directory(
            str(file_full_path.parent),
            file_full_path.name,
            as_attachment=True
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    # Get default downloads directory (user-writable location)
    from youtube_downloader import get_default_downloads_dir
    default_downloads = get_default_downloads_dir()
    
    print("\n" + "="*60)
    print("YouTube to MP3 Downloader - Web Interface")
    print("="*60)
    print(f"Downloads folder: {default_downloads}")
    print("Starting server on http://localhost:5000")
    print("Press Ctrl+C to stop")
    print("="*60 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)

