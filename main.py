import logging
from aiogram import Bot, Dispatcher, executor
from src.api_tokens import PyWeather_bot
from src.message_handlers import register_handlers

BOT_TOKEN = PyWeather_bot
logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

# запускаем функции из src.message_handler.py
register_handlers(dp)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
