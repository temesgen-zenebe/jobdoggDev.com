# Generated by Django 4.2 on 2023-06-10 03:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0015_remove_military_certification_license_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='military',
            name='slug',
            field=models.SlugField(default='slug', max_length=200),
        ),
    ]