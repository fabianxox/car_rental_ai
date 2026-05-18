from fastapi import APIRouter, Request

router = APIRouter()


@router.get("/webhook")
async def verify_webhook(request: Request):

    return {"status": "webhook verification endpoint"}