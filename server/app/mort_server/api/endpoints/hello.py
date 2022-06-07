from typing import Any

from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def hello(message: str) -> Any:
    return {"message": f"Your message said {message}"}
