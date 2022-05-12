from sqlalchemy.ext.asyncio import AsyncSession
from models.song_models import Song
from models.video_models import Video
from starlette.status import HTTP_201_CREATED
from fastapi.responses import JSONResponse


async def create_song_from_youtube(info: dict, session: AsyncSession):
    title = info.get('title')
    youtube_id = info.get('id')
    if '-' in title:
        artist = title[0:title.find('-')]
        name = title[title.find('-')+2:]
    else:
        artist = title
        name = title

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
            'id': song.song_id,
            'name': song.name
        }
    )


async def create_video_from_youtube(info: dict, session: AsyncSession):
    title = info.get('title')
    youtube_id = info.get('id')
    creator = info.get('creator')

    video = Video(
        name=title,
        youtube_id=youtube_id,
        creator=creator
    )

    session.add(video)
    await session.commit()
    await session.refresh(video)

    return JSONResponse(
        status_code=HTTP_201_CREATED,
        content={
            'message': 'Video created',
            'id': video.video_id,
            'name': video.name

        }
    )

