from typing import Optional

from sqlmodel import SQLModel, Field


class SongBase(SQLModel):
    name: str
    artist: str
    year: Optional[int] = None


class Song(SongBase, table=True):
    song_id: int = Field(default=None, primary_key=True)

    __table_args__ = {'schema': 'music'}


class SongCreate(SongBase):
    pass
