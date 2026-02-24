from aiogram import Router, F
from aiogram.types import CallbackQuery
from keyboards.keyboards import faq_menu, faq_back
from data.services import FAQ

router = Router()


@router.callback_query(F.data == "faq")
async def show_faq(callback: CallbackQuery):
    await callback.message.edit_text(
        "❓ <b>Частые вопросы</b>\n\n"
        "Выбери вопрос который тебя интересует 👇",
        reply_markup=faq_menu(),
        parse_mode="HTML"
    )
    await callback.answer()


@router.callback_query(F.data.startswith("faq_"))
async def show_faq_answer(callback: CallbackQuery):
    idx = int(callback.data.replace("faq_", ""))

    if idx >= len(FAQ):
        await callback.answer("Вопрос не найден")
        return

    item = FAQ[idx]
    await callback.message.edit_text(
        f"{item['q']}\n\n{item['a']}",
        reply_markup=faq_back(),
        parse_mode="HTML"
    )
    await callback.answer()
