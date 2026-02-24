from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from keyboards.keyboards import (
    order_services, order_budget, order_deadline,
    order_confirm, after_order, back_main, main_menu
)
from data.services import SERVICES
from config import ADMIN_ID, ADMIN_USERNAME

router = Router()


class OrderState(StatesGroup):
    choosing_service = State()
    entering_description = State()
    choosing_budget = State()
    choosing_deadline = State()
    confirming = State()


# Старт заявки из главного меню
@router.callback_query(F.data == "order")
async def start_order(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await state.set_state(OrderState.choosing_service)
    await callback.message.edit_text(
        "📝 <b>Оформление заявки</b>\n\n"
        "Шаг 1 из 4 — Выбери нужную услугу 👇",
        reply_markup=order_services(),
        parse_mode="HTML"
    )
    await callback.answer()


# Старт заявки с конкретной услуги
@router.callback_query(F.data.startswith("order_from_"))
async def start_order_from_service(callback: CallbackQuery, state: FSMContext):
    key = callback.data.replace("order_from_", "")
    service = SERVICES.get(key)
    await state.clear()
    await state.update_data(service=key, service_name=service["name"])
    await state.set_state(OrderState.entering_description)

    await callback.message.edit_text(
        f"📝 <b>Заявка: {service['name']}</b>\n\n"
        f"Шаг 2 из 4 — Опиши свою задачу подробнее:\n\n"
        f"<i>Например: нужен бот для приёма заявок с сайта, "
        f"чтобы клиент мог выбрать услугу и оставить контакт. "
        f"Уведомления должны приходить мне в Telegram.</i>\n\n"
        f"✍️ Напиши в свободной форме:",
        parse_mode="HTML",
        reply_markup=back_main()
    )
    await callback.answer()


# Выбор услуги
@router.callback_query(F.data.startswith("order_service_"), OrderState.choosing_service)
async def choose_service(callback: CallbackQuery, state: FSMContext):
    key = callback.data.replace("order_service_", "")
    service = SERVICES.get(key)
    await state.update_data(service=key, service_name=service["name"])
    await state.set_state(OrderState.entering_description)

    await callback.message.edit_text(
        f"✅ Услуга: <b>{service['name']}</b>\n\n"
        f"Шаг 2 из 4 — Опиши свою задачу подробнее:\n\n"
        f"<i>Чем подробнее опишешь — тем точнее я оценю стоимость и сроки.</i>\n\n"
        f"✍️ Напиши в свободной форме:",
        parse_mode="HTML",
        reply_markup=back_main()
    )
    await callback.answer()


# Получение описания
@router.message(OrderState.entering_description)
async def enter_description(message: Message, state: FSMContext):
    if len(message.text) < 10:
        await message.answer(
            "✏️ Пожалуйста, опиши задачу подробнее (хотя бы пару предложений)"
        )
        return

    await state.update_data(description=message.text)
    await state.set_state(OrderState.choosing_budget)

    await message.answer(
        "✅ Отлично!\n\n"
        "Шаг 3 из 4 — Укажи примерный бюджет 👇",
        reply_markup=order_budget(),
        parse_mode="HTML"
    )


# Выбор бюджета
BUDGET_LABELS = {
    "budget_5k": "до 5 000 ₽",
    "budget_15k": "5 000 — 15 000 ₽",
    "budget_50k": "15 000 — 50 000 ₽",
    "budget_50k+": "50 000 ₽+",
    "budget_discuss": "Обсудим",
}

@router.callback_query(F.data.startswith("budget_"), OrderState.choosing_budget)
async def choose_budget(callback: CallbackQuery, state: FSMContext):
    budget = BUDGET_LABELS.get(callback.data, "Не указан")
    await state.update_data(budget=budget)
    await state.set_state(OrderState.choosing_deadline)

    await callback.message.edit_text(
        f"✅ Бюджет: <b>{budget}</b>\n\n"
        f"Шаг 4 из 4 — Как срочно нужно? 👇",
        reply_markup=order_deadline(),
        parse_mode="HTML"
    )
    await callback.answer()


# Выбор срока
DEADLINE_LABELS = {
    "deadline_urgent": "⚡ Срочно (1–3 дня)",
    "deadline_normal": "🕐 Стандартно (1–2 недели)",
    "deadline_relax": "📅 Не горит (до месяца)",
}

@router.callback_query(F.data.startswith("deadline_"), OrderState.choosing_deadline)
async def choose_deadline(callback: CallbackQuery, state: FSMContext):
    deadline = DEADLINE_LABELS.get(callback.data, "Не указано")
    await state.update_data(deadline=deadline)
    await state.set_state(OrderState.confirming)

    data = await state.get_data()

    summary = (
        "📋 <b>Проверь заявку перед отправкой:</b>\n\n"
        f"🔧 <b>Услуга:</b> {data['service_name']}\n"
        f"📝 <b>Задача:</b> {data['description']}\n"
        f"💰 <b>Бюджет:</b> {data['budget']}\n"
        f"⏱ <b>Срок:</b> {deadline}\n\n"
        "Всё верно?"
    )

    await callback.message.edit_text(
        summary,
        reply_markup=order_confirm(),
        parse_mode="HTML"
    )
    await callback.answer()


# Отправка заявки
@router.callback_query(F.data == "order_submit", OrderState.confirming)
async def submit_order(callback: CallbackQuery, state: FSMContext, bot: Bot):
    data = await state.get_data()
    user = callback.from_user

    # Формируем сообщение для админа
    admin_msg = (
        "🔔 <b>НОВАЯ ЗАЯВКА!</b>\n\n"
        f"👤 <b>Клиент:</b> {user.full_name}\n"
        f"🆔 <b>Username:</b> @{user.username or 'нет'}\n"
        f"🔗 <b>ID:</b> <code>{user.id}</code>\n\n"
        f"🔧 <b>Услуга:</b> {data['service_name']}\n"
        f"📝 <b>Задача:</b>\n{data['description']}\n\n"
        f"💰 <b>Бюджет:</b> {data['budget']}\n"
        f"⏱ <b>Срок:</b> {data['deadline']}\n\n"
        f"💬 <b>Написать клиенту:</b> tg://user?id={user.id}"
    )

    try:
        await bot.send_message(ADMIN_ID, admin_msg, parse_mode="HTML")
    except Exception as e:
        print(f"Ошибка отправки заявки: {e}")

    await state.clear()

    await callback.message.edit_text(
        "✅ <b>Заявка отправлена!</b>\n\n"
        f"Я получил твою заявку и свяжусь с тобой в течение часа.\n\n"
        f"Если хочешь написать напрямую — {ADMIN_USERNAME}",
        reply_markup=after_order(),
        parse_mode="HTML"
    )
    await callback.answer("Заявка отправлена! ✅")
