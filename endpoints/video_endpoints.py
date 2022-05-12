from config import video_opts
import os
from pathlib import Path
from database import get_session
from models.video_models import Video, VideoCreate
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from endpoints.user_endpoints import auth_handler
from fastapi import APIRouter, Depends, HTTPException, Request
from starlette.status import HTTP_404_NOT_FOUND
from fastapi.responses import StreamingResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from yt_dlp import YoutubeDL
from services.youtube_services import create_video_from_youtube

video_router = APIRouter(
    dependencies=[Depends(auth_handler.auth_wrapper)],
    tags=['videos']
)

video_path = Path("/video/The Stains of Time-Ep7Ni6dtQaA.mp4")
templates = Jinja2Templates(directory='video_template')


@video_router.get('/get_video_from_youtube_url')
async def get_video_from_youtube_url(
        url: str = None,
        session: AsyncSession = Depends(get_session)):
    if os.path.exists('./video'):
        pass
    else:
        os.mkdir('./video')

    with YoutubeDL(video_opts) as ydl:
        info = ydl.extract_info(url=url, download=True)

        return await create_video_from_youtube(info=info, session=session)


@video_router.get('/videos', response_model=list[Video])
async def get_videos(session: AsyncSession = Depends(get_session)) -> list[Video]:
    result = await session.execute(select(Video))

    videos = result.scalars().all()

    return [Video(
        name=video.name,
        creator=video.creator,
        video_id=video.video_id,
        year=video.year,
        youtube_id=video.youtube_id
    )
        for video in videos]


@video_router.post('/videos')
async def add_video(video: VideoCreate,
                    session: AsyncSession = Depends(get_session)) -> Video:
    video = Video(name=video.name, creator=video.creator, youtube_id=video.youtube_id)
    session.add(video)
    await session.commit()
    await session.refresh(video)
    return video


@video_router.get('/get_video/{video_id}')
async def get_video(video_id: int,
                    session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Video).where(Video.video_id == video_id))
    video: Video = result.scalars().first()

    if not video:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail='Video is not found')

    youtube_id = video.youtube_id

    video_file = open(f'./video/{youtube_id}.mp4', mode='rb')
    return StreamingResponse(video_file, media_type='video/mp4')


@video_router.get('/stream_video/{video_id}', response_class=HTMLResponse)
async def stream_video(request: Request, video_id: int):
    return templates.TemplateResponse('index.htm', context={"request": request, "video_id": video_id})
