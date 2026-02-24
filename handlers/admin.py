from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from config import ADMIN_ID

router = Router()


def is_admin(user_id: int) -> bool:
    return user_id == ADMIN_ID


@router.message(Command("admin"))
async def admin_panel(message: Message):
    if not is_admin(message.from_user.id):
        await message.answer("⛔ Нет доступа")
        return

    await message.answer(
        "⚙️ <b>Панель администратора</b>\n\n"
        "Доступные команды:\n"
        "/admin — эта панель\n"
        "/stats — статистика (в разработке)\n\n"
        "Все заявки от клиентов приходят сюда автоматически 📬",
        parse_mode="HTML"
    )


@router.message(Command("stats"))
async def admin_stats(message: Message):
    if not is_admin(message.from_user.id):
        await message.answer("⛔ Нет доступа")
        return

    await message.answer(
        "📊 <b>Статистика</b>\n\n"
        "Функция в разработке.\n"
        "Пока все заявки приходят прямо в этот чат 👆",
        parse_mode="HTML"
    )
