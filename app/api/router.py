from fastapi import APIRouter

from app.api.routes import auth, music, playlists

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(music.router, prefix="", tags=["music"])
api_router.include_router(playlists.router, prefix="/playlists", tags=["playlists"])
