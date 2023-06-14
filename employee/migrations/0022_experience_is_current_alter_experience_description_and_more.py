# Generated by Django 4.2 on 2023-06-12 00:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0021_experience'),
    ]

    operations = [
        migrations.AddField(
            model_name='experience',
            name='is_current',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='experience',
            name='description',
            field=models.TextField(blank=True, help_text='tell about your specific roles', max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='experience',
            name='end_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]