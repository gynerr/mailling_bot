from asgiref.sync import sync_to_async
from celery import shared_task

from bot.utils import send_telegram_message
from ..django_admin_panel.celery import app


@app.task()
async def check_and_send_telegram_message():
    from .models import AdminResponse
    messages = await sync_to_async(list)(AdminResponse.objects.filter(needs_sending=True).select_related('message_id__user_id'))
    for message in messages:
        await send_telegram_message(message)
        message.needs_sending = False
        await sync_to_async(message.save)()
