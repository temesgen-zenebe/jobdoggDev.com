# Generated by Django 4.2 on 2023-07-14 22:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0042_alter_rettingcommenting_retting_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='videoresume',
            name='tell_about_you',
            field=models.TextField(blank=True, help_text='Share a fascinating fact or story about yourself.', max_length=600, null=True),
        ),
    ]
