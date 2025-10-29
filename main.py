from fastapi import FastAPI
from controllers import post, auth
from database import database, metadata, engine
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    from models.post import posts  # noqa

    await database.connect()
    metadata.create_all(engine)

    yield
    await database.disconnect()


app = FastAPI(lifespan=lifespan)
app.include_router(auth.router)
app.include_router(post.router)
