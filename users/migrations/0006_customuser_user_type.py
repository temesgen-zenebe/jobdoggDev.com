# Generated by Django 4.2 on 2023-05-28 19:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_customuser_is_employee_customuser_is_employer'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='user_type',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
