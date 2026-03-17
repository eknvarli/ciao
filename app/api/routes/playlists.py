from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from typing import List

from app.db.session import get_db
from app.db.models import Playlist, User, TrackRef
from app.api.dependencies.auth import get_current_user
from app.schemas.playlist import PlaylistCreate, PlaylistRead
from app.schemas.track import TrackRefDBRead

router = APIRouter()

@router.post("/", response_model=PlaylistRead, status_code=201)
async def create_playlist(
    playlist_in: PlaylistCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    playlist = Playlist(
        name=playlist_in.name,
        description=playlist_in.description,
        owner_id=current_user.id
    )
    db.add(playlist)
    await db.commit()
    await db.refresh(playlist)
    return playlist

@router.get("/", response_model=List[PlaylistRead])
async def read_playlists(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    stmt = select(Playlist).where(Playlist.owner_id == current_user.id).offset(skip).limit(limit)
    result = await db.execute(stmt)
    return result.scalars().all()

@router.get("/{playlist_id}", response_model=PlaylistRead)
async def read_playlist(
    playlist_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    stmt = select(Playlist).options(selectinload(Playlist.tracks)).where(
        (Playlist.id == playlist_id) & (Playlist.owner_id == current_user.id)
    )
    result = await db.execute(stmt)
    playlist = result.scalars().first()
    
    if not playlist:
        raise HTTPException(status_code=404, detail="Playlist not found")
    return playlist

@router.post("/{playlist_id}/tracks")
async def add_track_to_playlist(
    playlist_id: str,
    track_in: TrackRefDBRead,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    stmt = select(Playlist).options(selectinload(Playlist.tracks)).where(
        (Playlist.id == playlist_id) & (Playlist.owner_id == current_user.id)
    )
    result = await db.execute(stmt)
    playlist = result.scalars().first()
    
    if not playlist:
        raise HTTPException(status_code=404, detail="Playlist not found")
        
    stmt_track = select(TrackRef).where(TrackRef.id == track_in.id)
    result_track = await db.execute(stmt_track)
    track = result_track.scalars().first()
    
    if not track:
         track = TrackRef(
             id=track_in.id,
             title=track_in.title,
             artist=track_in.artist,
             duration=track_in.duration,
             thumbnail_url=track_in.thumbnail_url
         )
         db.add(track)
         
    if track not in playlist.tracks:
        playlist.tracks.append(track)
        await db.commit()
        
    return {"status": "ok"}
