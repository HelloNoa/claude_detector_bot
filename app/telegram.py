import httpx

from app.config import settings

TELEGRAM_API = f"https://api.telegram.org/bot{settings.telegram_bot_token}"


async def send_message(text: str) -> dict:
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            f"{TELEGRAM_API}/sendMessage",
            json={
                "chat_id": settings.telegram_chat_id,
                "text": text,
                "parse_mode": "HTML",
            },
        )
        return resp.json()