import os
from datetime import datetime

from aiogram import Bot
from aiogram.enums import ParseMode
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.date import DateTrigger
from dotenv import load_dotenv
from sqlalchemy import select, update

from bot.db.engine import async_session_maker
from db.engine import meta

load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')
bot = Bot(TOKEN, parse_mode=ParseMode.HTML)


async def get_all_users():
    user = meta.tables['bot_botuser']
    async with async_session_maker() as session:
        result = await session.execute(select(user))
        usr = result.fetchall()
    return usr


async def filtered_users(last_msg_date_from, last_msg_date_on,first_msg_date_from,first_msg_date_on):
    user = meta.tables['bot_botuser']
    async with async_session_maker() as session:
        result = await session.execute(
            select(user).where(
                (user.c.last_message_date < last_msg_date_on) &
                (user.c.last_message_date > last_msg_date_from) &
                (user.c.first_message_date < first_msg_date_on) &
                (user.c.first_message_date > first_msg_date_from)
            )
        )
        users = result.fetchall()
        return users


# async def get_mailings():
#     mailings = meta.tables['bot_mailing']
#     async with async_session_maker() as session:
#         result = await session.execute(select(mailings).where(mailings.c.needs_sending))
#         all_mailings = result.fetchall()
#     return all_mailings


async def send_all_messages(message: str, users):
    users = await get_all_users()
    for user in users:
        await bot.send_message(chat_id=user.tg_id, text=message)


async def schedule_maker(scheduler: AsyncIOScheduler):
    # mailings = await get_mailings()
    mailings = meta.tables['bot_mailing']
    async with async_session_maker() as session:
        result = await session.execute(select(mailings).where(mailings.c.needs_sending))
        all_mailings = result.fetchall()
        if all_mailings:
            for mail in all_mailings:
                time = mail.time
                date = mail.date
                message = mail.text
                last_message_from = mail.last_message_from
                last_message_on = mail.last_message_on
                first_message_from = mail.first_message_from
                first_message_on = mail.first_message_on
                users = await filtered_users(last_message_from, last_message_on, first_message_from, first_message_on)
                scheduled_time = datetime.combine(date, time)
                scheduler.add_job(send_all_messages, DateTrigger(run_date=scheduled_time), args=(message, users))
                await session.execute(update(mailings).where(mailings.c.id == mail.id).values(needs_sending=False))
            await session.commit()

#
# async def main():
#     await setup_database()
#     await schedule_maker()
#     while True:
#         schedule.run_pending()
#         time.sleep(1)
#
#
# if __name__ == '__main__':
#     asyncio.run(main())
