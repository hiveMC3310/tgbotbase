from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from structlog import get_logger

from filters import IsAdminFilter

logger = get_logger()

router = Router()


@router.message(Command("admin"), IsAdminFilter())
async def admin_start(message: Message):
    await message.answer(f"👮♂️ Admin command executed!")
