from django.contrib import admin

# Register your models here.
from .models import BotUser, UserMessage, AdminResponse, Mailing


class UserMessageAdmin(admin.ModelAdmin):
    list_display = ['user_id', 'text', 'date_created']


class AdminResponseAdmin(admin.ModelAdmin):
    list_display = ['message_id', 'response_text', 'date_created']


admin.site.register(BotUser)
admin.site.register(UserMessage, UserMessageAdmin)
admin.site.register(AdminResponse, AdminResponseAdmin)
admin.site.register(Mailing)
