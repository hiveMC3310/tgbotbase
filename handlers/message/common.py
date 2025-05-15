from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from structlog import get_logger

from keyboards.inline import common_inline_kb

logger = get_logger()

router = Router()


@router.message(CommandStart())
async def start_command(message: Message):
    await message.answer(f"👋 Hello, {message.from_user.first_name}", reply_markup=common_inline_kb())
