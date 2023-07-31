# Generated by Django 4.2 on 2023-07-31 00:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('employee', '0056_employeepreferences_work_arrangement_preference_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='skillsettestresult',
            name='conformation',
            field=models.CharField(default='', max_length=20),
        ),
        migrations.CreateModel(
            name='TaxDocumentSetting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('taxUserType', models.CharField(choices=[('employee', 'Employee'), ('contractor', 'Contractor/Freelancer')], max_length=20)),
                ('formType', models.CharField(choices=[('w-4', 'W-4'), ('w-9', 'W-9')], max_length=5)),
                ('uploadedDocuments', models.FileField(upload_to='taxDocuments/%Y/%m/%d')),
                ('states', models.CharField(choices=[('valid', 'Valid'), ('invalid', 'Invalid'), ('pending', 'Pending')], default='pending', max_length=10)),
                ('slug', models.SlugField(unique=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
