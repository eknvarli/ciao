import asyncio
from ytmusicapi import YTMusic
from app.schemas.track import TrackSearchItem

ytmusic = YTMusic()

def _parse_thumbnail(thumbnails: list) -> str:
    if not thumbnails:
        return ""

    sorted_thumbs = sorted(thumbnails, key=lambda x: x.get('width', 0) * x.get('height', 0))
    return sorted_thumbs[-1]['url'] if sorted_thumbs else ""

def _search_sync(query: str) -> list[dict]:
    results = ytmusic.search(query=query, filter="songs", limit=20)
    parsed = []
    for r in results:
        vid = r.get('videoId')
        if not vid:
           continue
        artists = r.get('artists')
        artist_name = artists[0].get('name') if artists else "Unknown Artist"
        
        parsed.append({
            "videoId": vid,
            "title": r.get('title', 'Unknown Title'),
            "artist": artist_name,
            "duration": r.get('duration_seconds', 0),
            "thumbnail_url": _parse_thumbnail(r.get('thumbnails', []))
        })
    return parsed

def _get_track_sync(video_id: str) -> dict:
    track = ytmusic.get_song(video_id)
    vid_details = track.get('videoDetails', {})
    if not vid_details:
        return {}
        
    return {
        "videoId": vid_details.get('videoId'),
        "title": vid_details.get('title'),
        "artist": vid_details.get('author'),
        "duration": int(vid_details.get('lengthSeconds', 0)),
        "thumbnail_url": _parse_thumbnail(vid_details.get('thumbnail', {}).get('thumbnails', [])),
    }
    
class YTMusicService:
    @staticmethod
    async def search_tracks(query: str) -> list[dict]:
        return await asyncio.to_thread(_search_sync, query)

    @staticmethod
    async def get_track(video_id: str) -> dict:
         return await asyncio.to_thread(_get_track_sync, video_id)
