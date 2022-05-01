from config import opts
import os
from database import get_session
from models.song_models import Song, SongCreate
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from endpoints.user_endpoints import auth_handler
from fastapi import APIRouter, Depends, HTTPException
from starlette.status import HTTP_404_NOT_FOUND
from fastapi.responses import StreamingResponse, FileResponse
from yt_dlp import YoutubeDL
from services.song_services import create_song_from_youtube

song_router = APIRouter(dependencies=[Depends(auth_handler.auth_wrapper)],
                        tags=['songs'])


@song_router.get('/get_audio_from_youtube_url')
async def get_audio_from_youtube_url(url: str = None,
                                     session: AsyncSession = Depends(get_session)):

    if os.path.exists('./music/from_youtube'):
        pass
    else:
        os.mkdir('./music')
        os.mkdir('./music/from_youtube')

    with YoutubeDL(opts) as ydl:
        info = ydl.extract_info(url=url, download=True)

        return await create_song_from_youtube(info=info, session=session)


@song_router.get('/songs', response_model=list[Song])
async def get_songs(session: AsyncSession = Depends(get_session)) -> list[Song]:
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
                   session: AsyncSession = Depends(get_session)) -> Song:
    song = Song(name=song.name, artist=song.artist)
    session.add(song)
    await session.commit()
    await session.refresh(song)
    return song


@song_router.get('/get_song')
async def get_song(song_name: str,
                   session: AsyncSession = Depends(get_session)):

    result = await session.execute(select(Song).where(Song.name.ilike(f'%{song_name}%')))
    song: Song = result.scalars().first()

    if not song:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail='Song is not found')

    video_id = song.youtube_id

    for file in os.listdir('./music/from_youtube'):
        if video_id in file:

            return FileResponse(f'./music/from_youtube/{file}')

