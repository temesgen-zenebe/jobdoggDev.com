# Generated by Django 4.2 on 2023-05-02 07:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testimonial', '0002_rename_views_count_testimonial_view_count_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='testimonial',
            name='image',
            field=models.URLField(blank=True, null=True),
        ),
    ]
