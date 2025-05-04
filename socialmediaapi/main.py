from fastapi import FastAPI

from socialmediaapi.routers.post import router as post_router

app = FastAPI()

app.include_router(post_router)
