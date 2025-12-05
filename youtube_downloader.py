#!/usr/bin/env python3
"""
YouTube Video/Playlist Downloader and MP3 Converter
Downloads YouTube videos or entire playlists and converts them to MP3 at 172kbps
"""

import os
import sys
import json
import shutil
from pathlib import Path
import yt_dlp
from threading import Lock

# Global lock for thread-safe operations
download_lock = Lock()

# Check if running in PyInstaller bundle
def is_frozen():
    return getattr(sys, 'frozen', False)


def find_ffmpeg():
    """
    Try to find FFmpeg executable in common locations or PATH
    Returns the path to ffmpeg executable or None if not found
    """
    # Check if ffmpeg is in PATH
    ffmpeg_path = shutil.which('ffmpeg')
    if ffmpeg_path:
        return ffmpeg_path
    
    # Check bundled FFmpeg (if installed with the application)
    if getattr(sys, 'frozen', False):
        # Running in a bundle (PyInstaller)
        base_path = Path(sys.executable).parent
    else:
        base_path = Path(__file__).parent
    
    bundled_paths = [
        base_path / "ffmpeg" / "bin" / "ffmpeg.exe",
        base_path / "ffmpeg" / "ffmpeg.exe",
    ]
    for path in bundled_paths:
        if path.exists():
            return str(path)
    
    # Common Windows installation paths
    if sys.platform == 'win32':
        common_paths = [
            r'C:\ffmpeg\bin\ffmpeg.exe',
            r'C:\Program Files\ffmpeg\bin\ffmpeg.exe',
            r'C:\Program Files (x86)\ffmpeg\bin\ffmpeg.exe',
            r'C:\Program Files\YouTube to MP3 Downloader\ffmpeg\bin\ffmpeg.exe',
            os.path.expanduser(r'~\ffmpeg\bin\ffmpeg.exe'),
        ]
        for path in common_paths:
            if os.path.exists(path):
                return path
    
    return None


def get_default_downloads_dir():
    """
    Get the default downloads directory (user-writable location)
    """
    if sys.platform == 'win32':
        # Use Documents folder on Windows
        downloads_dir = Path(os.path.expanduser('~')) / 'Documents' / 'YouTube Downloads'
    else:
        # Use home directory on other platforms
        downloads_dir = Path(os.path.expanduser('~')) / 'YouTube Downloads'
    
    # Create directory if it doesn't exist
    try:
        downloads_dir.mkdir(parents=True, exist_ok=True)
    except PermissionError:
        # Fallback to current directory if Documents is not accessible
        downloads_dir = Path('downloads')
        try:
            downloads_dir.mkdir(exist_ok=True)
        except PermissionError:
            # Last resort: use temp directory
            import tempfile
            downloads_dir = Path(tempfile.gettempdir()) / 'YouTube Downloads'
            downloads_dir.mkdir(parents=True, exist_ok=True)
    
    return downloads_dir


class YouTubeDownloader:
    def __init__(self, output_dir=None, bitrate="172k", ffmpeg_path=None):
        """
        Initialize the YouTube downloader
        
        Args:
            output_dir: Directory to save downloaded files (default: user's Documents/YouTube Downloads)
            bitrate: Audio bitrate for MP3 conversion (default: 172k)
            ffmpeg_path: Optional path to FFmpeg executable
        """
        if output_dir is None:
            output_dir = get_default_downloads_dir()
        elif output_dir == "downloads":
            # If user specifies "downloads", use the default location
            output_dir = get_default_downloads_dir()
        
        self.output_dir = Path(output_dir)
        try:
            self.output_dir.mkdir(parents=True, exist_ok=True)
        except PermissionError as e:
            raise Exception(
                f"Permission denied: Cannot create downloads folder at '{self.output_dir}'. "
                f"Please choose a different location or run as administrator."
            ) from e
        
        self.bitrate = bitrate
        self.progress_callback = None
        
        # Find FFmpeg
        if ffmpeg_path:
            self.ffmpeg_path = ffmpeg_path
        else:
            self.ffmpeg_path = find_ffmpeg()
        
        if not self.ffmpeg_path:
            raise Exception(
                "FFmpeg not found! Please install FFmpeg and add it to your PATH, "
                "or provide the path using --ffmpeg-location. "
                "See FFMPEG_SETUP.md for installation instructions."
            )
        
    def set_progress_callback(self, callback):
        """Set a callback function for progress updates"""
        self.progress_callback = callback
        
    def progress_hook(self, d):
        """Hook for yt-dlp progress updates"""
        if self.progress_callback:
            if d['status'] == 'downloading':
                total = d.get('total_bytes') or d.get('total_bytes_estimate', 0)
                downloaded = d.get('downloaded_bytes', 0)
                if total > 0:
                    percent = (downloaded / total) * 100
                    self.progress_callback({
                        'status': 'downloading',
                        'percent': percent,
                        'speed': d.get('speed', 0),
                        'eta': d.get('eta', 0)
                    })
            elif d['status'] == 'finished':
                self.progress_callback({
                    'status': 'converting',
                    'percent': 100
                })
    
    def get_ydl_opts(self, playlist=False, playlist_items=None):
        """
        Get yt-dlp options for downloading and converting to MP3
        
        Args:
            playlist: Whether downloading a playlist (affects output template)
            playlist_items: Optional list of playlist indices to download (1-indexed)
        
        Returns:
            Dictionary of yt-dlp options
        """
        if playlist:
            # For playlists: organize by playlist name, then track number - title
            output_template = str(self.output_dir / "%(playlist_title)s" / "%(playlist_index)s - %(title)s.%(ext)s")
        else:
            # For single videos: just use the title
            output_template = str(self.output_dir / "%(title)s.%(ext)s")
        
        opts = {
            'format': 'bestaudio/best',  # Get best audio quality available
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': self.bitrate.replace('k', ''),  # yt-dlp expects just the number
            }],
            'outtmpl': output_template,
            'quiet': False,
            'no_warnings': False,
            'extractaudio': True,
            'audioformat': 'mp3',
            'embed_subs': False,
            'writesubtitles': False,
            'writeautomaticsub': False,
            'progress_hooks': [self.progress_hook],
            'ffmpeg_location': self.ffmpeg_path,
            'ignoreerrors': True,  # Continue on download errors (skip unavailable videos)
            'no_warnings': False,
        }
        
        # Add playlist selection if specified
        if playlist and playlist_items:
            # yt-dlp uses 1-indexed playlist items, format: "1,3,5" or "1-5"
            if isinstance(playlist_items, list):
                opts['playlist_items'] = ','.join(map(str, playlist_items))
            else:
                opts['playlist_items'] = str(playlist_items)
        
        return opts
    
    def get_video_info(self, url):
        """
        Get video/playlist information without downloading
        
        Args:
            url: YouTube URL (video or playlist)
        
        Returns:
            Dictionary with video/playlist information
        """
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'ignoreerrors': True,  # Continue on download errors (unavailable videos)
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                
                if 'entries' in info:  # Playlist
                    entries = []
                    unavailable_count = 0
                    available_index = 1
                    
                    # Process each entry - None entries are unavailable
                    for idx, entry in enumerate(info['entries']):
                        original_index = idx + 1
                        
                        if entry is None:
                            unavailable_count += 1
                            # Still add it to the list but mark as unavailable (use original index for display)
                            entries.append({
                                'index': -1,  # Negative index indicates unavailable
                                'original_index': original_index,
                                'title': 'Unavailable Video',
                                'duration': 0,
                                'url': '',
                                'id': '',
                                'available': False
                            })
                        else:
                            # Entry is available
                            entries.append({
                                'index': available_index,
                                'original_index': original_index,
                                'title': entry.get('title', 'Unknown'),
                                'duration': entry.get('duration', 0),
                                'url': entry.get('url', ''),
                                'id': entry.get('id', ''),
                                'available': True
                            })
                            available_index += 1
                    
                    available_count = len([e for e in entries if e.get('available', True)])
                    
                    return {
                        'type': 'playlist',
                        'title': info.get('title', 'Unknown Playlist'),
                        'count': available_count,
                        'unavailable_count': unavailable_count,
                        'videos': entries
                    }
                else:  # Single video
                    # Check if single video is available
                    if info is None or not info.get('title'):
                        raise Exception("This video is unavailable. It may have been removed or is blocked in your country.")
                    
                    return {
                        'type': 'video',
                        'title': info.get('title', 'Unknown'),
                        'duration': info.get('duration', 0),
                        'thumbnail': info.get('thumbnail', ''),
                        'uploader': info.get('uploader', 'Unknown'),
                        'view_count': info.get('view_count', 0),
                        'available': True
                    }
        except yt_dlp.utils.DownloadError as e:
            error_msg = str(e)
            if 'unavailable' in error_msg.lower() or 'blocked' in error_msg.lower() or 'copyright' in error_msg.lower():
                raise Exception("This video is unavailable. It may have been removed or is blocked in your country.")
            raise Exception(f"Error fetching video info: {str(e)}")
        except Exception as e:
            error_msg = str(e)
            if 'unavailable' in error_msg.lower() or 'blocked' in error_msg.lower():
                raise Exception("This video is unavailable. It may have been removed or is blocked in your country.")
            raise Exception(f"Error fetching video info: {str(e)}")
    
    def download(self, url, progress_callback=None, selected_indices=None):
        """
        Download YouTube video or playlist
        
        Args:
            url: YouTube URL (video or playlist)
            progress_callback: Optional callback function for progress updates
            selected_indices: Optional list of playlist indices to download (1-indexed)
        """
        if progress_callback:
            self.set_progress_callback(progress_callback)
        
        # Check if URL is a playlist
        is_playlist = 'playlist' in url.lower() or 'list=' in url.lower()
        
        ydl_opts = self.get_ydl_opts(playlist=is_playlist, playlist_items=selected_indices)
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                # Extract info first
                info = ydl.extract_info(url, download=False)
                
                # If playlist with selected items, filter the count
                if is_playlist and selected_indices:
                    actual_count = len(selected_indices)
                elif is_playlist:
                    actual_count = info.get('playlist_count', len(info.get('entries', [])))
                else:
                    actual_count = 1
                
                result = {
                    'success': True,
                    'type': 'playlist' if is_playlist else 'video',
                    'title': info.get('title', 'Unknown') if not is_playlist else info.get('title', 'Unknown Playlist'),
                    'count': actual_count,
                    'output_dir': str(self.output_dir.absolute())
                }
                
                # Download
                ydl.download([url])
                
                return result
                
        except yt_dlp.utils.DownloadError as e:
            raise Exception(f"Download error: {str(e)}")
        except Exception as e:
            raise Exception(f"Unexpected error: {str(e)}")


def main():
    """CLI interface for the downloader"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Download YouTube videos or playlists and convert to MP3 at 172kbps',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Download a single video
  python youtube_downloader.py "https://www.youtube.com/watch?v=VIDEO_ID"
  
  # Download a playlist
  python youtube_downloader.py "https://www.youtube.com/playlist?list=PLAYLIST_ID"
  
  # Custom output directory
  python youtube_downloader.py "URL" --output "my_music"
  
  # Custom bitrate
  python youtube_downloader.py "URL" --bitrate "192k"
        """
    )
    
    parser.add_argument(
        'url',
        help='YouTube video or playlist URL'
    )
    
    parser.add_argument(
        '--output', '-o',
        default='downloads',
        help='Output directory for downloaded files (default: downloads)'
    )
    
    parser.add_argument(
        '--bitrate', '-b',
        default='172k',
        help='Audio bitrate for MP3 conversion (default: 172k)'
    )
    
    args = parser.parse_args()
    
    # Validate bitrate format
    if not args.bitrate.endswith('k'):
        print("Error: Bitrate must end with 'k' (e.g., '172k', '192k')")
        sys.exit(1)
    
    downloader = YouTubeDownloader(
        output_dir=args.output,
        bitrate=args.bitrate
    )
    
    try:
        result = downloader.download(args.url)
        print(f"\n{'='*60}")
        print("Download and conversion completed successfully!")
        print(f"Type: {result['type']}")
        print(f"Title: {result['title']}")
        print(f"Files saved to: {result['output_dir']}")
        print(f"{'='*60}\n")
    except Exception as e:
        print(f"\nError: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()

