# Generated by Django 5.0.4 on 2024-04-30 18:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0002_alter_project_author_alter_project_contents'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='contents',
            field=models.JSONField(blank=True, null=True),
        ),
    ]