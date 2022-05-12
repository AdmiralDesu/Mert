from typing import Optional
from sqlmodel import SQLModel, Field


class SongBase(SQLModel):
    name: str = Field(nullable=False, index=True)
    artist: str = Field(nullable=False, index=True)
    year: Optional[int] = Field(default=None)
    youtube_id: str = Field(default=None, index=True)


class Song(SongBase, table=True):
    song_id: int = Field(nullable=False, primary_key=True)

    __table_args__ = {'schema': 'songs'}


class SongCreate(SongBase):
    pass
