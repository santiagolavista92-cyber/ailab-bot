import os

# ===================================
# НАСТРОЙКИ БОТА
# ===================================

# --- BOT TOKEN ---
BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError("❌ BOT_TOKEN не найден в переменных окружения!")

# --- ADMIN ID ---
admin_id_raw = os.getenv("ADMIN_ID")

if not admin_id_raw:
    raise ValueError("❌ ADMIN_ID не найден в переменных окружения!")

try:
    ADMIN_ID = int(admin_id_raw)
except ValueError:
    raise ValueError("❌ ADMIN_ID должен быть числом!")

# --- Дополнительные настройки ---
ADMIN_USERNAME = "@Saintbeat_bot"
SITE_URL = "https://telegrambotai.ru"
