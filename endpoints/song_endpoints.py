from config import opts
import os
from database import get_session
from models.song_models import Song, SongCreate
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from endpoints.user_endpoints import auth_handler
from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse, FileResponse
from yt_dlp import YoutubeDL

song_router = APIRouter(dependencies=[Depends(auth_handler.auth_wrapper)], tags=['songs'])


@song_router.get('/get_audio_from_youtube_url')
async def get_audio_from_youtube_url(url: str = None, user=Depends(auth_handler.auth_wrapper)) -> FileResponse:

    if os.path.exists('./music'):
        pass
    else:
        os.mkdir('./music')

    with YoutubeDL(opts) as ydl:
        info_dict = ydl.extract_info(url=url, download=True)
        video_id = info_dict.get('id')
        for file in os.listdir('./music'):
            if video_id in file:
                filename = file.title()
    return FileResponse(f'./music/{filename}')


@song_router.get('/songs', response_model=list[Song])
async def get_songs(session: AsyncSession = Depends(get_session),
                    user=Depends(auth_handler.auth_wrapper)) -> list[Song]:
    result = await session.execute(select(Song))

    songs = result.scalars().all()

    return [Song(
        name=song.name,
        artist=song.artist,
        song_id=song.song_id,
        year=song.year
    )
        for song in songs]


@song_router.post('/songs')
async def add_song(song: SongCreate,
                   session: AsyncSession = Depends(get_session),
                   user=Depends(auth_handler.auth_wrapper)) -> Song:
    song = Song(name=song.name, artist=song.artist)
    session.add(song)
    await session.commit()
    await session.refresh(song)
    return song
