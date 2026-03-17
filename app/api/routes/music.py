from fastapi import APIRouter, Depends, HTTPException, Request
from typing import List

from slowapi import Limiter
from slowapi.util import get_remote_address

from app.services.ytmusic_service import YTMusicService
from app.services.stream_service import StreamService
from app.core.cache import cache_response
from app.schemas.track import TrackSearchItem, TrackDetail
from app.schemas.stream import StreamResponse

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)

@router.get("/search", response_model=List[TrackSearchItem])
@limiter.limit("30/minute")
@cache_response(ttl=900)
async def search_music(request: Request, q: str):
    if not q:
        return []
    try:
        results = await YTMusicService.search_tracks(q)
        return results
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Error communicating with upstream service: {e}")

@router.get("/tracks/{video_id}", response_model=TrackDetail)
@cache_response(ttl=3600)
async def get_track_info(video_id: str):
    try:
        info = await YTMusicService.get_track(video_id)
        if not info:
             raise HTTPException(status_code=404, detail="Track not found")
        return info
    except Exception as e:
         raise HTTPException(status_code=502, detail=f"Error communicating with upstream service: {e}")

@router.get("/streams/{video_id}", response_model=StreamResponse)
@cache_response(ttl=300)
async def get_stream(video_id: str):
    try:
        stream_data = await StreamService.get_stream_data(video_id)
        if not stream_data or not stream_data.get("stream_url"):
            raise HTTPException(status_code=404, detail="Stream not found")
        return stream_data
    except Exception as e:
         raise HTTPException(status_code=500, detail=f"Error extracting stream: {e}")
