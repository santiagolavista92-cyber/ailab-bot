import os

# ===================================
# НАСТРОЙКИ БОТА
# ===================================

# Токен берётся из переменной окружения (Railway)
# или напрямую если запускаешь локально
BOT_TOKEN = os.getenv("BOT_TOKEN", "ТВОЙ_ТОКЕН_ЗДЕСЬ")

# Твой Telegram ID (получи у @userinfobot)
ADMIN_ID = int(os.getenv("ADMIN_ID", "123456789"))

# Ссылка на тебя для связи
ADMIN_USERNAME = "@Saintbeat_bot"

# Ссылка на сайт
SITE_URL = "https://telegrambotai.ru"
