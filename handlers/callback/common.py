from aiogram import F, Router
from aiogram.types import CallbackQuery
from structlog import get_logger

logger = get_logger()

router = Router()


@router.callback_query(F.data == "click")
async def start_command(callback: CallbackQuery):
    await callback.message.edit_text("Button clicked!")
    await callback.answer(f"{callback.from_user.first_name} clicked")
