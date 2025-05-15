from aiogram import Dispatcher

from config_reader import Settings
from middlewares import *


def setup_dispatcher(config: Settings) -> Dispatcher:
    dp = Dispatcher()

    # Middlewares
    dp.message.middleware(LoggingMiddleware())
    dp.callback_query.middleware(LoggingMiddleware())
    dp.update.outer_middleware(AdminsMiddleware(config.bot.admins))

    return dp
