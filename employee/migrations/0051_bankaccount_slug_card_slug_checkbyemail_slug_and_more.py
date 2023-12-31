# Generated by Django 4.2 on 2023-07-25 01:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0050_ewallet_checkbyemail_card_bankaccount'),
    ]

    operations = [
        migrations.AddField(
            model_name='bankaccount',
            name='slug',
            field=models.SlugField(default='bankmineacc', unique=True),
        ),
        migrations.AddField(
            model_name='card',
            name='slug',
            field=models.SlugField(default='cardmineacc', unique=True),
        ),
        migrations.AddField(
            model_name='checkbyemail',
            name='slug',
            field=models.SlugField(default='checkby', unique=True),
        ),
        migrations.AddField(
            model_name='ewallet',
            name='slug',
            field=models.SlugField(default='ewallettype', unique=True),
        ),
    ]
