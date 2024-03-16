from asgiref.sync import sync_to_async
from celery import shared_task
import logging
from bot.utils import send_telegram_message

logger = logging.getLogger(__name__)

#
# @shared_task(name='django_admin_panel.bot.tasks.check_and_send_telegram_message')
async def check_and_send_telegram_message():
    try:
        from .models import AdminResponse
        messages = await sync_to_async(list)(
            AdminResponse.objects.filter(needs_sending=True).select_related('message_id__user_id'))
        for message in messages:
            await send_telegram_message(message)
            message.needs_sending = False
            await sync_to_async(message.save)()
    except Exception as e:
        logger.exception('An error occurred in check_and_send_telegram_message task: %s', e)

# @shared_task(name='django_admin_panel.bot.tasks.check_and_send_telegram_message')
# def check_and_send_telegram_message():
#     from .models import AdminResponse
#     messages = AdminResponse.objects.filter(needs_sending=True).select_related('message_id__user_id')
#     for message in messages:
#         sync_to_async(send_telegram_message(message))
# #         message.needs_sending = False
#         sync_to_async(message.save)()
