from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from endpoints.user_endpoints import user_router
from endpoints.song_endpoints import song_router
from endpoints.video_endpoints import video_router

app = FastAPI()
app.include_router(user_router)
app.include_router(song_router)
app.include_router(video_router)


@app.get('/')
async def front_tab():
    return RedirectResponse(f'/docs')


