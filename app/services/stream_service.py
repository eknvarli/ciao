import asyncio
import yt_dlp

def _extract_stream_url_sync(video_id: str) -> dict:
    url = f"https://www.youtube.com/watch?v={video_id}"
    
    ydl_opts = {
        'format': 'bestaudio[ext=m4a]/bestaudio[ext=webm]/bestaudio/best',
        'quiet': True,
        'no_warnings': True,
        'skip_download': True,
        'youtube_include_dash_manifest': False,
        'extract_flat': False
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(url, download=False)

            formats = info.get('formats', [])

            if not formats:
                raise Exception("No formats found")

            audio_formats = [
                f for f in formats
                if f.get("acodec") != "none" and f.get("vcodec") == "none"
            ]

            if not audio_formats:
                raise Exception("No audio formats found")

            best_audio = max(audio_formats, key=lambda f: f.get("abr") or 0)
            stream_url = best_audio.get("url")
            
            if not stream_url:
                raise Exception("Could not determine stream URL")
                
            thumbnails = info.get('thumbnails', [])
            best_thumbnail = ""
            if thumbnails:
                best_thumb = max(thumbnails, key=lambda t: t.get("width", 0) * t.get("height", 0))
                best_thumbnail = best_thumb.get("url", "")
                
            return {
                "stream_url": stream_url,
                "title": info.get("title", "Unknown Title"),
                "artist": info.get("uploader", "Unknown Artist"),
                "thumbnail": best_thumbnail
            }

        except Exception as e:
            raise Exception(f"Failed to extract stream for {video_id}: {str(e)}")


class StreamService:
    @staticmethod
    async def get_stream_data(video_id: str) -> dict:
        return await asyncio.to_thread(_extract_stream_url_sync, video_id)