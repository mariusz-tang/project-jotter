# Generated by Django 5.0.4 on 2024-04-30 18:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0003_alter_project_contents'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='completed',
            field=models.BooleanField(blank=True, default=False),
        ),
    ]
