from typing import Optional
from sqlmodel import SQLModel, Field


class VideoBase(SQLModel):
    name: str = Field(nullable=False, index=True)
    creator: str = Field(nullable=False, index=True)
    year: Optional[int] = Field(default=None)
    youtube_id: str = Field(default=None, index=True)


class Video(VideoBase, table=True):
    video_id: int = Field(nullable=False, primary_key=True, index=True)

    __table_args__ = {'schema': 'videos'}


class VideoCreate(VideoBase):
    pass
