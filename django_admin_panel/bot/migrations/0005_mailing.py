# Generated by Django 5.0.2 on 2024-02-22 18:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0004_adminresponse_date_created_usermessage_date_created'),
    ]

    operations = [
        migrations.CreateModel(
            name='Mailing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('time', models.TimeField()),
                ('text', models.TextField()),
            ],
        ),
    ]
