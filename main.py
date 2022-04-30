import os
from fastapi.responses import StreamingResponse, FileResponse
from yt_dlp import YoutubeDL
from fastapi import Depends, FastAPI
from config import opts
from database import init_db, get_session
from models.models import Song, SongCreate
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

app = FastAPI()


@app.get('/get_audio_from_youtube_url')
async def get_audio_from_youtube_url(url: str = None) -> FileResponse:

    with YoutubeDL(opts) as ydl:
        info_dict = ydl.extract_info(url=url, download=True)
        video_id = info_dict.get('id')
        for file in os.listdir('./music'):
            if video_id in file:
                filename = file.title()
    return FileResponse(f'./music/{filename}')


@app.get('/songs', response_model=list[Song])
async def get_songs(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Song))

    songs = result.scalars().all()

    return [Song(name=song.name, artist=song.artist, song_id=song.song_id, year=song.year) for song in songs]


@app.post('/songs')
async def add_song(song: SongCreate, session: AsyncSession = Depends(get_session)):
    song = Song(name=song.name, artist=song.artist)
    session.add(song)
    await session.commit()
    await session.refresh(song)
    return song


