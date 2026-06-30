import os
import tempfile
import urllib.request
import traceback
from pytubefix import YouTube

class AudioExtractor:
    """
    A Zero-legacy service class for extracting audio from YouTube videos.
    Utilizes pytubefix with automatic PoToken generation to bypass datacenter blocks.
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
        url = f"https://www.youtube.com/watch?v={video_id}"
        
        # Initialize YouTube object with WEB client to trigger PoToken generation
        # use_po_token=True allows pytubefix to invoke node.js to generate the token.
        yt = YouTube(url, client='WEB', use_po_token=True)
        
        title = yt.title or "Unknown Title"
        artist = yt.author or "Unknown Artist"
        duration = yt.length or 0
        
        # Filter for m4a/mp4 audio streams and order by highest bitrate
        audio_streams = yt.streams.filter(only_audio=True, subtype='mp4').order_by('abr').desc()
        
        if not audio_streams:
            # Fallback to any audio if mp4/m4a isn't available
            audio_streams = yt.streams.filter(only_audio=True).order_by('abr').desc()
            
        if not audio_streams:
            raise Exception("No audio streams found for this video.")
            
        best_audio = audio_streams.first()
        
        # Download the file
        out_filename = f"audio_{video_id}.m4a"
        audio_path = best_audio.download(output_path=self.temp_dir, filename=out_filename)
        
        # Handle Thumbnail
        thumb_path = None
        if yt.thumbnail_url:
            thumb_filename = f"thumb_{video_id}.jpg"
            thumb_path = os.path.join(self.temp_dir, thumb_filename)
            try:
                # Add headers for thumbnail fetch
                req = urllib.request.Request(
                    yt.thumbnail_url, 
                    headers={'User-Agent': 'Mozilla/5.0'}
                )
                with urllib.request.urlopen(req, timeout=10) as response, open(thumb_path, 'wb') as out_file:
                    out_file.write(response.read())
            except Exception as e:
                print(f"Failed to download thumbnail: {e}")
                thumb_path = None

        return {
            'audio_path': audio_path,
            'title': title,
            'artist': artist,
            'duration': duration,
            'thumb_path': thumb_path
        }
