from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from data.services import SERVICES, FAQ


def main_menu() -> InlineKeyboardMarkup:
    """Главное меню"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💼 Услуги и цены", callback_data="services")],
        [InlineKeyboardButton(text="📝 Оставить заявку", callback_data="order")],
        [InlineKeyboardButton(text="❓ Частые вопросы", callback_data="faq")],
        [InlineKeyboardButton(text="🌐 Перейти на сайт", url="https://telegrambotai.ru")],
    ])


def services_menu() -> InlineKeyboardMarkup:
    """Меню услуг"""
    buttons = []
    for key, svc in SERVICES.items():
        buttons.append([
            InlineKeyboardButton(
                text=f"{svc['emoji']} {svc['name'].replace(svc['emoji'] + ' ', '')} — {svc['price_text']}",
                callback_data=f"service_{key}"
            )
        ])
    buttons.append([InlineKeyboardButton(text="◀️ Назад", callback_data="back_main")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def service_detail(service_key: str) -> InlineKeyboardMarkup:
    """Кнопки под описанием услуги"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📝 Хочу это — оставить заявку", callback_data=f"order_from_{service_key}")],
        [InlineKeyboardButton(text="◀️ Назад к услугам", callback_data="services")],
    ])


def faq_menu() -> InlineKeyboardMarkup:
    """Меню FAQ"""
    buttons = []
    for i, item in enumerate(FAQ):
        buttons.append([
            InlineKeyboardButton(text=item["q"], callback_data=f"faq_{i}")
        ])
    buttons.append([InlineKeyboardButton(text="◀️ Назад", callback_data="back_main")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def faq_back() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="◀️ К вопросам", callback_data="faq")],
        [InlineKeyboardButton(text="📝 Оставить заявку", callback_data="order")],
    ])


def order_services() -> InlineKeyboardMarkup:
    """Выбор услуги при оформлении заявки"""
    buttons = []
    for key, svc in SERVICES.items():
        buttons.append([
            InlineKeyboardButton(
                text=f"{svc['emoji']} {svc['name'].replace(svc['emoji'] + ' ', '')}",
                callback_data=f"order_service_{key}"
            )
        ])
    buttons.append([InlineKeyboardButton(text="❌ Отмена", callback_data="back_main")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def order_budget() -> InlineKeyboardMarkup:
    """Выбор бюджета"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="до 5 000 ₽", callback_data="budget_5k")],
        [InlineKeyboardButton(text="5 000 — 15 000 ₽", callback_data="budget_15k")],
        [InlineKeyboardButton(text="15 000 — 50 000 ₽", callback_data="budget_50k")],
        [InlineKeyboardButton(text="50 000 ₽+", callback_data="budget_50k+")],
        [InlineKeyboardButton(text="Не знаю / обсудим", callback_data="budget_discuss")],
    ])


def order_deadline() -> InlineKeyboardMarkup:
    """Выбор срочности"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⚡ Срочно (1–3 дня)", callback_data="deadline_urgent")],
        [InlineKeyboardButton(text="🕐 Стандартно (1–2 недели)", callback_data="deadline_normal")],
        [InlineKeyboardButton(text="📅 Не горит (до месяца)", callback_data="deadline_relax")],
    ])


def order_confirm() -> InlineKeyboardMarkup:
    """Подтверждение заявки"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Отправить заявку", callback_data="order_submit")],
        [InlineKeyboardButton(text="✏️ Изменить", callback_data="order")],
        [InlineKeyboardButton(text="❌ Отмена", callback_data="back_main")],
    ])


def back_main() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🏠 Главное меню", callback_data="back_main")],
    ])


def after_order() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🌐 Посмотреть сайт", url="https://telegrambotai.ru")],
        [InlineKeyboardButton(text="🏠 Главное меню", callback_data="back_main")],
    ])
