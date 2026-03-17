import uuid
from datetime import datetime
from typing import List, Optional
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, DateTime, Boolean, ForeignKey, Table, Column

from app.db.session import Base

playlist_track_association = Table(
    "playlist_track",
    Base.metadata,
    Column("playlist_id", ForeignKey("playlists.id", ondelete="CASCADE"), primary_key=True),
    Column("track_id", ForeignKey("tracks.id", ondelete="CASCADE"), primary_key=True)
)

class User(Base):
    __tablename__ = "users"
    
    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    email: Mapped[str] = mapped_column(String, unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    
    playlists: Mapped[List["Playlist"]] = relationship("Playlist", back_populates="owner", cascade="all, delete-orphan")

class Playlist(Base):
    __tablename__ = "playlists"
    
    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name: Mapped[str] = mapped_column(String)
    description: Mapped[Optional[str]] = mapped_column(String)
    owner_id: Mapped[str] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    
    owner: Mapped["User"] = relationship("User", back_populates="playlists")
    tracks: Mapped[List["TrackRef"]] = relationship("TrackRef", secondary=playlist_track_association, back_populates="playlists")

class TrackRef(Base):
    __tablename__ = "tracks"
    
    id: Mapped[str] = mapped_column(String, primary_key=True)
    title: Mapped[str] = mapped_column(String)
    artist: Mapped[str] = mapped_column(String)
    duration: Mapped[int] = mapped_column(Integer, default=0)
    thumbnail_url: Mapped[Optional[str]] = mapped_column(String)
    
    playlists: Mapped[List["Playlist"]] = relationship("Playlist", secondary=playlist_track_association, back_populates="tracks")
