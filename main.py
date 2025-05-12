from asyncio import run
from telegram_bot.bot import dp, bot
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    logger.info('Running')
    run(main())