from fastapi import FastAPI
from endpoints.user_endpoints import user_router
from endpoints.song_endpoints import song_router

app = FastAPI()
app.include_router(user_router)
app.include_router(song_router)




