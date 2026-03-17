import asyncio
import yt_dlp

def _extract_stream_url_sync(video_id: str) -> str:
    url = f"https://www.youtube.com/watch?v={video_id}"
    
    ydl_opts = {
        'format': 'bestaudio[ext=m4a]/bestaudio/best',
        'quiet': True,
        'no_warnings': True,
        'skip_download': True,
        'youtube_include_dash_manifest': False,
        'extract_flat': False
        }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(url, download=False)
            return info.get('url', "")
        except Exception as e:
            print(f"Error extracting stream for {video_id}: {e}")
            return ""

class StreamService:
    @staticmethod
    async def get_stream_url(video_id: str) -> str:
        return await asyncio.to_thread(_extract_stream_url_sync, video_id)
