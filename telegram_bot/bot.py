from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message
import logging
import os
from langchain_ollama import ChatOllama
from langchain_core.messages.ai import AIMessage
from mcp_use import MCPAgent, MCPClient
import os
import re
from dotenv import load_dotenv
from asyncio import run

logger = logging.getLogger(__name__)

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
OLLAMA_URL = os.getenv("OLLAMA_URL")
CONFIG = {
      "mcpServers": {
        "Appointment Booking Assistant": {
            "command": "mcp",
            "args": [
                "run",
                "mcp_server.py"
            ]
            }
      }
    }

SYSTEM_PROMPT = """
Use /nothink for every user prompt.
"""

client = MCPClient.from_dict(CONFIG)
llm = ChatOllama(model="qwen3:8b", base_url=OLLAMA_URL)
agent = MCPAgent(llm=llm, client=client, max_steps=30, system_prompt=SYSTEM_PROMPT)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

def parse_result(result: str) -> str:
    pattern = r"<think>.*?</think>"
    cleaned_text = re.sub(pattern, "", result, flags=re.DOTALL)
    return cleaned_text.strip()


async def ask(message: str) -> str:
    content = await agent.run(message)
    result = AIMessage(content)
    return parse_result(result.content)

@dp.message(CommandStart())
async def start_command(message: Message):
    await message.answer(f"Hello, {message.from_user.first_name}! I'm your bot.")

@dp.message()
async def ask_llm(message: Message):
    message_text = message.text
    await bot.send_chat_action(message.chat.id, "typing")
    print(message_text)
    response = await ask(message_text)
    await message.answer(response, parse_mode="HTML")
    
async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    logger.info('Running')
    run(main())