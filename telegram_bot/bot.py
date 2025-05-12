from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message
from bridge.main import ask
import logging
import os

logger = logging.getLogger(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def start_command(message: Message):
    await message.answer(f"Hello, {message.from_user.first_name}! I'm your bot.")

@dp.message()
async def ask_llm(message: Message):
    message_text = "/nothink " + message.text
    await bot.send_chat_action(message.chat.id, "typing")
    response = await ask(message_text)
    await message.answer(response, parse_mode="Markdown")