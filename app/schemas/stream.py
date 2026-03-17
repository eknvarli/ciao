from pydantic import BaseModel

class StreamResponse(BaseModel):
    stream_url: str
    title: str
    artist: str
    thumbnail: str
