from fastapi import APIRouter

from mort_server.api.endpoints import hello

router = APIRouter()

router.include_router(
    hello.router,
    prefix="/hello",
    tags=["Hello"]
)
