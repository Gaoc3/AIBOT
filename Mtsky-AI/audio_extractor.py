import os
import tempfile
import urllib.request
import traceback
import yt_dlp

class AudioExtractor:
    """
    A Zero-legacy service class for extracting audio from YouTube videos.
    Utilizes yt-dlp wrapped cleanly to decouple audio extraction from the bot logic.
    """
    
    def __init__(self):
        self.temp_dir = tempfile.gettempdir()
        
    def download_audio(self, video_id: str):
        """
        Downloads the highest quality m4a audio for a given YouTube video ID.
        Returns:
            dict: {
                'audio_path': str,
                'title': str,
                'artist': str,
                'duration': int,
                'thumb_path': str (or None)
            }
        """
        video_url = f"https://www.youtube.com/watch?v={video_id}"
        out_tmpl = os.path.join(self.temp_dir, f"audio_{video_id}.%(ext)s")
        thumb_path = os.path.join(self.temp_dir, f"thumb_{video_id}.jpg")
        
        ydl_opts = {
            'format': 'bestaudio[ext=m4a]/bestaudio/best',
            'outtmpl': out_tmpl,
            'quiet': True,
            'nocheckcertificate': True,
            'http_chunk_size': 2097152,
            'concurrent_fragment_downloads': 10,
            'socket_timeout': 15,
            'retries': 3,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'm4a',
                'preferredquality': '192',
            }]
        }
        
        audio_file_m4a = os.path.join(self.temp_dir, f"audio_{video_id}.m4a")

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=True)
            title = info.get('title', 'Unknown Title')
            artist = info.get('uploader', 'Unknown Artist')
            duration = info.get('duration', 0)
            url_thumb = info.get('thumbnail')
            audio_path = audio_file_m4a

        if url_thumb:
            try:
                req = urllib.request.Request(
                    url_thumb, 
                    headers={'User-Agent': 'Mozilla/5.0'}
                )
                with urllib.request.urlopen(req, timeout=10) as response, open(thumb_path, 'wb') as out_file:
                    out_file.write(response.read())
            except Exception as e:
                print(f"Failed to download thumbnail: {e}")
                thumb_path = None
        else:
            thumb_path = None

        return {
            'audio_path': audio_path,
            'title': title,
            'artist': artist,
            'duration': duration,
            'thumb_path': thumb_path
        }
