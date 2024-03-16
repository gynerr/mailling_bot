from datetime import datetime

from django.db import models

# Create your models here.
from django.utils import timezone


class BotUser(models.Model):
    tg_id = models.IntegerField()
    first_name = models.CharField(max_length=20, blank=True, null=True)
    last_name = models.CharField(max_length=25, blank=True, null=True)
    username = models.CharField(max_length=30)
    last_message_date = models.DateField(default=timezone.now)
    first_message_date = models.DateField(default=timezone.now)

    def __str__(self):
        return self.username

    def update_last_message_date(self):
            self.last_message_date = timezone.now()
            self.save()

    class Meta:
        app_label = 'bot'


class UserMessage(models.Model):
    user_id = models.ForeignKey(BotUser, on_delete=models.CASCADE, related_name='user')
    text = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text

    class Meta:
        app_label = 'bot'


class AdminResponse(models.Model):
    message_id = models.ForeignKey(UserMessage, on_delete=models.CASCADE, related_name='user_message')
    response_text = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    needs_sending = models.BooleanField(default=True)

    class Meta:
        app_label = 'bot'


class Mailing(models.Model):
    date = models.DateField()
    time = models.TimeField()
    text = models.TextField()
    needs_sending = models.BooleanField(default=True)
    last_message_from = models.DateField(default=timezone.now)
    last_message_on = models.DateField(default=timezone.now)
    first_message_from = models.DateField(default=timezone.now)
    first_message_on = models.DateField(default=timezone.now)

    def __str__(self):
        return self.text

    class Meta:
        app_label = 'bot'
