import logging

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.formatter import format_message
from app.schemas import StatusPageWebhook
from app.telegram import send_message

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Claude Status Bot")


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/webhook")
async def webhook(payload: StatusPageWebhook, request: Request):
    logger.info("Webhook received: %s", payload.model_dump_json())

    text = format_message(payload)
    result = await send_message(text)

    if not result.get("ok"):
        logger.error("Telegram send failed: %s", result)
        return JSONResponse(status_code=502, content={"error": "telegram_send_failed"})

    return {"ok": True}