from sqlalchemy.ext.asyncio import AsyncSession
from models.song_models import Song
from starlette.status import HTTP_201_CREATED
from fastapi.responses import JSONResponse


async def create_song_from_youtube(info: dict, session: AsyncSession):
    title = info.get('title')
    youtube_id = info.get('id')
    artist = title[0:title.find('-')]
    name = title[title.find('-')+2:]

    song = Song(
        name=name,
        artist=artist,
        youtube_id=youtube_id
    )

    session.add(song)
    await session.commit()
    await session.refresh(song)

    return JSONResponse(
        status_code=HTTP_201_CREATED,
        content={
            'message': 'Song created',
            'name': name
        }
    )

