from typing import Optional
from sqlmodel import SQLModel, Field


class AlbumBase(SQLModel):
    album_name: str = Field(nullable=False, index=True)
    author: str = Field(nullable=False, index=True)
    year: Optional[int] = Field(nullable=False, index=True)
    songs: Optional[str] = Field(nullable=False)
    description: Optional[str] = Field(nullable=True)


class Album(AlbumBase, table=True):
    album_id: int = Field(nullable=False, primary_key=True, index=True)
    thumbnail_path: str = Field(default=None, index=True)

    __table_args__ = {'schema': 'songs'}


class AlbumCreate(AlbumBase):
    pass
