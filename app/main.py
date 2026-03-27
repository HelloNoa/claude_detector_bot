import logging
import time

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.formatter import format_message
from app.schemas import StatusPageWebhook
from app.telegram import send_message

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Claude Status Bot")

# 중복 웹훅 방지: {event_key: timestamp}
_seen: dict[str, float] = {}
DEDUP_TTL = 300  # 5분 내 동일 이벤트 무시


def _dedup_key(payload: StatusPageWebhook) -> str:
    if payload.incident:
        return f"incident:{payload.incident.id}:{payload.incident.updated_at}"
    if payload.component:
        cu = payload.component_update
        return f"component:{payload.component.id}:{cu.new_status if cu else ''}"
    return f"page:{payload.page.status_indicator if payload.page else ''}"


def _is_duplicate(key: str) -> bool:
    now = time.monotonic()
    # 오래된 항목 정리
    expired = [k for k, t in _seen.items() if now - t > DEDUP_TTL]
    for k in expired:
        del _seen[k]
    if key in _seen:
        return True
    _seen[key] = now
    return False


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/webhook")
async def webhook(payload: StatusPageWebhook, request: Request):
    key = _dedup_key(payload)

    if _is_duplicate(key):
        logger.info("Duplicate webhook ignored: %s", key)
        return {"ok": True, "skipped": "duplicate"}

    logger.info("Webhook received: %s", key)

    text = format_message(payload)
    result = await send_message(text)

    if not result.get("ok"):
        logger.error("Telegram send failed: %s", result)
        return JSONResponse(status_code=502, content={"error": "telegram_send_failed"})

    return {"ok": True}