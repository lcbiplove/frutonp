# Generated by Django 3.0.5 on 2020-09-10 04:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('join', '0003_remove_myuser_token'),
    ]

    operations = [
        migrations.AddField(
            model_name='myuser',
            name='is_activated',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='myuser',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
