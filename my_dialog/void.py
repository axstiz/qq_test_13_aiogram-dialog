from aiogram import Router, F
from aiogram.types import Message

# Создаём роутер и указываем, что он должен реагировать только на текстовые сообщения
router = Router()



@router.message(F.text)
async def handle_text(message: Message):
    await message.answer('prod. by dibuildo_group (axstiz - @litsummer)')