from aiogram import Router


def setup_routers() -> Router:
    from .callback import common as callback_common
    from .message import admin
    from .message import common as message_common

    router = Router()
    router.include_router(message_common.router)
    router.include_router(callback_common.router)
    router.include_router(admin.router)

    return router
