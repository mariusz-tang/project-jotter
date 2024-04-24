# Generated by Django 5.0.4 on 2024-04-24 20:33

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='given_name',
            field=models.CharField(blank=True, help_text='The name used to refer to the user in communications', max_length=150, verbose_name='preferred name'),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_verified',
            field=models.BooleanField(default=False, verbose_name='email verification status'),
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. The username must be at most 150 charactes long and consist solely of letters, numbers and @/./+/-/_.', max_length=150, unique=True, validators=[django.core.validators.RegexValidator(message='Please enter a valid username. This value may contain only letters, numbers, and @/./+/-/_ characters.', regex='^[\\w.@+-]+\\Z')]),
        ),
    ]
