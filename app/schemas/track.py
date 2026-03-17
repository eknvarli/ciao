from pydantic import BaseModel
from typing import Optional, List

class TrackSearchItem(BaseModel):
    videoId: str
    title: str
    artist: str
    duration: int
    thumbnail_url: Optional[str] = None

class TrackDetail(TrackSearchItem):
    album: Optional[str] = None

class TrackRefDBBase(BaseModel):
    id: str
    title: str
    artist: str
    duration: int
    thumbnail_url: Optional[str] = None

class TrackRefDBRead(TrackRefDBBase):
    model_config = {"from_attributes": True}
