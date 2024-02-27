import os
from datetime import datetime

import django
from aiogram import Bot
from aiogram.enums import ParseMode
from aiogram.types import Message
from dotenv import load_dotenv
from sqlalchemy import select, insert, MetaData, Engine
from sqlalchemy.ext.asyncio import AsyncSession

from bot.db import engine
from bot.db.engine import async_session_maker, meta


load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')
bot = Bot(TOKEN, parse_mode=ParseMode.HTML)

django.setup()

async def check_user(message: Message, meta):
    user = meta.tables['bot_botuser']
    async with async_session_maker() as session:
        result = await session.execute(select(user).where(user.c.tg_id == message.from_user.id))
        existing_user = result.fetchone()
        if existing_user is None:
            try:
                result = await session.execute(
                    insert(user).values(
                        tg_id=message.from_user.id,
                        first_name=message.from_user.first_name,
                        last_name=message.from_user.last_name,
                        username=message.from_user.username
                    )
                )
                await session.commit()
            except Exception as e:
                print("Error inserting data:", e)


async def add_user_messages(message: Message, meta):
    user = meta.tables['bot_botuser']
    user_messages = meta.tables['bot_usermessage']
    async with async_session_maker() as session:
        result = await session.execute(select(user).where(user.c.tg_id == message.from_user.id))
        usr = result.fetchone()
        await session.execute(
            insert(user_messages).values(user_id_id=usr.id, text=message.text, date_created=datetime.now()))
        await session.commit()


async def send_telegram_message(message):
    user_message = message.message_id
    bot_user = user_message.user_id
    await bot.send_message(chat_id=bot_user.tg_id, text=message.response_text)
