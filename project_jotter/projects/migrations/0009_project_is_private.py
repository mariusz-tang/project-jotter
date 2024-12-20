# Generated by Django 5.0.4 on 2024-05-05 18:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0008_alter_project_image_alter_project_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='is_private',
            field=models.BooleanField(blank=True, default=False, help_text='Private projects are not displayed to other users who visit your profile'),
        ),
    ]
