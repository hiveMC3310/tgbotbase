import logging
from contextlib import suppress
from pathlib import Path

import structlog
from aiogram import Bot
from structlog.types import FilteringBoundLogger

from config_reader import Settings
from dispatcher import setup_dispatcher
from handlers import setup_routers
from logs import get_structlog_config


async def main() -> None:
    config = Settings.from_toml(Path("config.toml"))

    structlog.configure(**get_structlog_config(config))

    bot = Bot(token=config.bot.token.get_secret_value())
    bot.config = config
    dp = setup_dispatcher(config)

    dp.include_router(setup_routers())

    logger: FilteringBoundLogger = structlog.get_logger()

    try:
        logger.info("Starting bot")
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    finally:
        await bot.session.close()
        logger.info("Bot stopped")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    with suppress(KeyboardInterrupt):
        import asyncio
        asyncio.run(main())
