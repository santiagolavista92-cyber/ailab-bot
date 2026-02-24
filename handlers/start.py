from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from keyboards.keyboards import main_menu

router = Router()

WELCOME_TEXT = (
    "👋 Привет! Я бот <b>AI Lab</b>\n\n"
    "Разрабатываю Telegram-боты, сайты и AI-решения <b>без предоплат</b> — "
    "сначала делаю, потом платишь.\n\n"
    "🤖 <b>Что умею:</b>\n"
    "— Рассказать об услугах и ценах\n"
    "— Принять заявку и передать разработчику\n"
    "— Ответить на частые вопросы\n\n"
    "Выбери что тебя интересует 👇"
)


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(
        WELCOME_TEXT,
        reply_markup=main_menu(),
        parse_mode="HTML"
    )


@router.callback_query(F.data == "back_main")
async def back_to_main(callback: CallbackQuery):
    await callback.message.edit_text(
        WELCOME_TEXT,
        reply_markup=main_menu(),
        parse_mode="HTML"
    )
    await callback.answer()
