from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from app.schemas.track import TrackRefDBRead

class PlaylistBase(BaseModel):
    name: str
    description: Optional[str] = None

class PlaylistCreate(PlaylistBase):
    pass

class PlaylistRead(PlaylistBase):
    id: str
    owner_id: str
    created_at: datetime
    tracks: List[TrackRefDBRead] = []

    model_config = {"from_attributes": True}
