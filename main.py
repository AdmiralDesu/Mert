import os
from fastapi import FastAPI
from fastapi.responses import StreamingResponse, FileResponse
from yt_dlp import YoutubeDL
from config import opts

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









