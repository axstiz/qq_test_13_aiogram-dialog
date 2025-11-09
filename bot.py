from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram_dialog import setup_dialogs
import asyncio

from my_dialog import void, linear_dialog, cyclic_dialog
from input_cfg import TOKEN



async def main():

    bot = Bot(token=TOKEN)
    dp = Dispatcher()

    # Регистрация диалога
    dp.include_routers(linear_dialog.dialog, cyclic_dialog.dialog, void.router)
    setup_dialogs(dp)

    # Регистрация команды /start
    dp.message.register(linear_dialog.start_dialog, Command("start"))
    dp.message.register(cyclic_dialog.start_help_dialog, Command("help"))

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
