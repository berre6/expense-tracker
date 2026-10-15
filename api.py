
from contextlib import asynccontextmanager

from fastapi import FastAPI

import database
from routers.expenses import router as expenses_router


def create_app(initialize_db: bool = True):
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        if initialize_db:
            database.init_db()
        yield

    app = FastAPI(lifespan=lifespan)
    app.include_router(expenses_router)

    @app.get("/")
    def home():
        return {"message": "Hello"}

    return app


app = create_app()





