from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from mort_server.api import api
from mort_server.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Mort Server API",
    openapi_url="/api/openapi.json",
)

if settings.CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(api.router, prefix="/api")
