from time import perf_counter
from typing import Any, Callable, Dict

import structlog
from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message, TelegramObject

logger = structlog.get_logger()


class LoggingMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Any],
        event: TelegramObject,
        data: Dict[str, Any],
    ):
        log_data = {"update_type": event.__class__.__name__}

        log_data["update_id"] = getattr(event, "update_id", None)

        if isinstance(event, Message):
            self._add_message_data(log_data, event)
        elif isinstance(event, CallbackQuery):
            self._add_callback_data(log_data, event)

        logger.debug("Update received", **log_data)

        start_time = perf_counter()

        try:
            result = await handler(event, data)
            log_data["execution_time"] = f"{perf_counter() - start_time:.3f}s"
            logger.info("Update processed", **log_data)
            return result
        except Exception as e:
            log_data.update({
                "error": str(e),
                "execution_time": f"{perf_counter() - start_time:.3f}s",
                "exception_type": e.__class__.__name__
            })
            logger.error("Update processing failed", **log_data)
            raise
        finally:
            structlog.contextvars.clear_contextvars()

    def _add_message_data(self, log_data: dict, message: Message) -> None:
        """Добавляем данные сообщения в контекст логирования"""
        user = getattr(message, "from_user", None)
        chat = getattr(message, "chat", None)

        log_data.update({
            "message_id": message.message_id,
            "user_id": user.id if user else None,
            "chat_id": chat.id if chat else None,
            "content_type": message.content_type,
            "text": message.text or message.caption,
        })

    def _add_callback_data(self, log_data: dict, callback: CallbackQuery) -> None:
        """Добавляем данные callback-запроса в контекст логирования"""
        user = getattr(callback, "from_user", None)
        message = getattr(callback, "message", None)

        log_data.update({
            "callback_data": callback.data,
            "user_id": user.id if user else None,
            "message_id": message.message_id if message else None,
        })
