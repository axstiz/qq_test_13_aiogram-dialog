from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Создаём кнопку с командой /help
help_button = KeyboardButton(text="/help")

# Создаём клавиатуру с одной кнопкой
help_reply_keyboard = ReplyKeyboardMarkup(
    keyboard=[[help_button]],
    resize_keyboard=True,  # Клавиатура подстроится под размер
    one_time_keyboard=False,  # Клавиатура останется, а не скроется после нажатия
    input_field_placeholder="Узнай что я могу"  # Подсказка в поле ввода
)