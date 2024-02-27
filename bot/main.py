import asyncio
import logging
import os
import sys

import django
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils.markdown import hbold
from django.utils import timezone
from dotenv import load_dotenv

from bot.utils import check_user, add_user_messages
from db.engine import setup_database, meta
from django_admin_panel.bot.tasks import check_and_send_telegram_message

load_dotenv()
# Bot token can be obtained via https://t.me/BotFather
TOKEN = os.getenv("BOT_TOKEN")

# All handlers should be attached to the Router (or Dispatcher)
dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    logging.info('Check')
    await check_user(message, meta)
    check_and_send_telegram_message.delay()
    await message.answer(f"Hello, {hbold(message.from_user.full_name)}!")



@dp.message()
async def echo_handler(message: types.Message) -> None:
    try:
        await check_user(message, meta)
        # Send a copy of the received message
        await message.answer(text='Доброго времени суток, администратор ответит на ваше сообщение когда будет в сети!')
        # await bot.send_message(chat_id=message.chat.id, message="Администратор ответит на ваше сообщение когда будет в сети")
        await add_user_messages(message, meta)
    except TypeError:
        # But not all the types is supported to be copied so need to handle it
        await message.answer("Nice try!")


# async def on_startup(dispatcher: Dispatcher):
#     meta.reflect(bind=engine)

async def main() -> None:
    # Initialize Bot instance with a default parse mode which will be passed to all API calls
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    # And the run events dispatching
    await setup_database()
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
