import time
from logging import getLogger
from fastapi import FastAPI, Request
from fastapi.concurrency import asynccontextmanager
from fastapi.responses import ORJSONResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware

from ai_health.root.app_routers import api
from ai_health.root.settings import Settings


LOGGER = getLogger(__file__)
settings = Settings()


def intialize() -> FastAPI:
    app = FastAPI(default_response_class=ORJSONResponse)

    ORIGINS = ["*"]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=ORIGINS,
        allow_credentials=False,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    app.include_router(router=api)

    return app


app = intialize()


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


@app.get("/")
def home():
    return RedirectResponse(url="/docs")
