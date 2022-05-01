from typing import Optional
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import UniqueConstraint, Column, String


class PlaylistBase(SQLModel):
    playlist_name: str
    year: Optional[int] = None
    songs: Optional[str] = None


class Playlist(PlaylistBase, table=True):
    playlist_id: int = Field(nullable=False, primary_key=True)
    thumbnail_path: str = Field(default=None)
    user_id: int = Field(foreign_key='users.user.user_id', nullable=False)

    __table_args__ = {'schema': 'users'}


class PlaylistCreate(PlaylistBase):
    pass
