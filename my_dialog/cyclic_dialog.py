
from aiogram import Bot, Dispatcher
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message
from aiogram_dialog import Dialog, DialogManager, StartMode, Window, setup_dialogs
from aiogram_dialog.widgets.kbd import SwitchTo, Row, Cancel
from aiogram_dialog.widgets.text import Const, Format
from aiogram.filters import Command


# --- Состояния диалога ---
class CyclicStates(StatesGroup):
    first = State()
    second = State()
    third = State()
    fourth = State()


# --- Геттер данных ---
async def get_data(dialog_manager: DialogManager, **kwargs):
    current_state = dialog_manager.current_context().state.state.split(":")[-1].upper()
    return {
        "current": current_state,
        "total": 4,
    }


# --- Функция запуска диалога по команде /help ---
async def start_help_dialog(message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(CyclicStates.first, mode=StartMode.RESET_STACK)


# --- Диалог ---
dialog = Dialog(
    Window(
        Const("📌 ШАГ 1 из 4\n\nДобро пожаловать в диалог помощи!"),
        Format("Текущее состояние: {current}"),
        Row(
            SwitchTo(Const("⬅️ Назад"), id="prev", state=CyclicStates.fourth),
            SwitchTo(Const("➡️ Вперед"), id="next", state=CyclicStates.second),# Цикл: 1 → 4
        ),
        state=CyclicStates.first,
        getter=get_data,
    ),
    Window(
        Const("📌 ШАГ 2 из 4\n\nВы на втором шаге — обучение продолжается."),
        Format("Текущее состояние: {current}"),
        Row(
            SwitchTo(Const("⬅️ Назад"), id="back", state=CyclicStates.first),
            SwitchTo(Const("➡️ Вперед"), id="next", state=CyclicStates.third),
        ),
        state=CyclicStates.second,
        getter=get_data,
    ),
    Window(
        Const("📌 ШАГ 3 из 4\n\nПодходим к финалу."),
        Format("Текущее состояние: {current}"),
        Row(
            SwitchTo(Const("⬅️ Назад"), id="back", state=CyclicStates.second),
            SwitchTo(Const("➡️ Вперед"), id="next", state=CyclicStates.fourth),
        ),
        state=CyclicStates.third,
        getter=get_data,
    ),
    Window(
        Const("📌 ШАГ 4 из 4\n\nВы прошли весь диалог!"),
        Format("Текущее состояние: {current}"),
        Row(
            SwitchTo(Const("⬅️ Назад"), id="back", state=CyclicStates.third),
            SwitchTo(Const("➡️ Вперед"), id="next", state=CyclicStates.first),  # Цикл: 4 → 1
        ),
        Cancel(Const("✅ Завершить")),
        state=CyclicStates.fourth,
        getter=get_data,
    ),
)