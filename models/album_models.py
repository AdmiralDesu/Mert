from typing import Optional
from sqlmodel import SQLModel, Field


class AlbumBase(SQLModel):
    album_name: str = Field(nullable=False, index=True)
    author: str = Field(nullable=False, index=True)
    year: Optional[int] = Field(nullable=False)
    songs: Optional[str] = Field(nullable=False)


class Album(AlbumBase, table=True):
    album_id: int = Field(nullable=False, primary_key=True)
    thumbnail_path: str = Field(default=None, index=True)

    __table_args__ = {'schema': 'music'}


class AlbumCreate(AlbumBase):
    pass
