# Generated by Django 2.2.4 on 2019-08-11 10:02

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Guess',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_email', models.EmailField(max_length=254, unique=True)),
                ('keyword', models.CharField(max_length=255)),
                ('number', models.IntegerField(validators=[django.core.validators.MinValueValidator(100), django.core.validators.MaxValueValidator(999)])),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
