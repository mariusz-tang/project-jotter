# Generated by Django 5.0.4 on 2024-05-07 14:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0009_project_is_private'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='completed',
        ),
        migrations.AddField(
            model_name='project',
            name='is_completed',
            field=models.BooleanField(blank=True, default=False, verbose_name='completed'),
        ),
        migrations.AlterField(
            model_name='project',
            name='is_private',
            field=models.BooleanField(blank=True, default=False, help_text='Private projects are not displayed to other users who visit your profile', verbose_name='private'),
        ),
    ]