# Generated by Django 5.2.1 on 2025-05-28 10:57

import accounts.models
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=254, unique=True),
        ),
        migrations.CreateModel(
            name='Code',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.PositiveIntegerField(default=accounts.models.generic_code)),
                ('exp_date', models.DateTimeField(default=accounts.models.exp_time_now)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='code', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
