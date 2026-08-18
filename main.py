import asyncio
import logging
import os

from config import API_HASH, API_ID, BOT_TOKEN, bot

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


def validate_environment():
    missing = []
    if not API_ID:
        missing.append("API_ID")
    if not API_HASH:
        missing.append("API_HASH")
    if not BOT_TOKEN:
        missing.append("BOT_TOKEN")
    if missing:
        raise RuntimeError(
            "Missing Railway variable(s): " + ", ".join(missing)
            + ". Add them under the service's Variables tab."
        )


async def main():
    validate_environment()
    os.makedirs("sessions", exist_ok=True)

    # Import plugins only after the client exists so their handlers can register safely.
    from plugins import register_all_handlers
    from telethon import events

    await bot.start(bot_token=BOT_TOKEN)
    register_all_handlers(bot)

    @bot.on(events.CallbackQuery)
    async def debug_cb(event):
        logger.debug("Callback data: %s", event.data)

    me = await bot.get_me()
    username = f"@{me.username}" if me.username else f"(no username, id={me.id})"
    logger.info("BOT STARTED: %s", username)
    logger.info("Telegram bot connected and handlers registered")
    await bot.run_until_disconnected()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped")
    except Exception:
        logger.exception("Bot failed during startup or runtime")
        raise
