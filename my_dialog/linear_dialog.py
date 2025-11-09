from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram_dialog import Dialog, DialogManager, StartMode, Window, setup_dialogs
from aiogram_dialog.widgets.kbd import Button, Cancel
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.input import TextInput
import asyncio

from reply_keyboards import help_reply_keyboard

# --- Состояния ---
from aiogram.fsm.state import StatesGroup, State


class LinearStates(StatesGroup):
    main = State()
    entering_name = State()


# --- Диалоговые функции ---
async def get_data(dialog_manager: DialogManager, **kwargs):
    return {"name": dialog_manager.dialog_data.get("name", "друг")}


async def on_name_entered(
        message: Message,
        widget: TextInput,
        dialog_manager: DialogManager,
        text: str,
):
    if len(text.strip()) < 3:
        await message.answer("❌ Имя слишком короткое! Пожалуйста, введите имя длиной не менее 3 букв.")
        return  # Остаемся в текущем состоянии, просим ввести снова

    dialog_manager.dialog_data["name"] = text.strip()
    await message.answer(f"Приятно познакомиться, {text.strip()}!", reply_markup=help_reply_keyboard)
    await dialog_manager.close_manager()



# --- Кнопка для перехода к вводу имени ---
async def on_input_name(
        callback: types.CallbackQuery,
        button: Button,
        dialog_manager: DialogManager,
):
    await dialog_manager.switch_to(LinearStates.entering_name)


# --- Создание диалога ---
dialog = Dialog(
    Window(
        Format("Привет, {name}! 👋\nНажми кнопку, чтобы представиться."),
        Button(Const("📝 Ввести имя"), id="input_name", on_click=on_input_name),
        Cancel(Const("❌ Выйти")),
        state=LinearStates.main,
        getter=get_data,
    ),
    Window(
        Const("Введите ваше имя:"),
        TextInput(id="name_input", on_success=on_name_entered),
        Cancel(Const("❌ Выйти")),
        state=LinearStates.entering_name,
    ),
)


# --- Обработчик команды /start ---

async def start_dialog(message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(LinearStates.main, mode=StartMode.RESET_STACK)