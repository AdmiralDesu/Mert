from typing import Optional
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import UniqueConstraint, Column, String


class PlaylistBase(SQLModel):
    playlist_name: str = Field(nullable=False, index=True)
    year: Optional[int] = Field(default=None)
    songs: Optional[str] = Field(default=None)


class Playlist(PlaylistBase, table=True):
    playlist_id: int = Field(nullable=False, primary_key=True)
    thumbnail_path: str = Field(default=None, index=True)
    user_id: int = Field(foreign_key='user.user_id', nullable=False, index=True)


class PlaylistCreate(PlaylistBase):
    pass
