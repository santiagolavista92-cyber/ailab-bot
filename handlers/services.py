from aiogram import Router, F
from aiogram.types import CallbackQuery
from keyboards.keyboards import services_menu, service_detail
from data.services import SERVICES

router = Router()


@router.callback_query(F.data == "services")
async def show_services(callback: CallbackQuery):
    text = (
        "💼 <b>Услуги и цены</b>\n\n"
        "Цены стартуют от минимума — итоговая стоимость "
        "зависит от сложности твоей задачи и ТЗ.\n\n"
        "Выбери что интересует 👇"
    )
    await callback.message.edit_text(
        text,
        reply_markup=services_menu(),
        parse_mode="HTML"
    )
    await callback.answer()


@router.callback_query(F.data.startswith("service_"))
async def show_service_detail(callback: CallbackQuery):
    key = callback.data.replace("service_", "")
    service = SERVICES.get(key)

    if not service:
        await callback.answer("Услуга не найдена")
        return

    await callback.message.edit_text(
        service["description"],
        reply_markup=service_detail(key),
        parse_mode="HTML"
    )
    await callback.answer()
