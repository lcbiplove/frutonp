# Generated by Django 3.0.5 on 2020-07-03 10:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_auto_20200701_1131'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='photos', to='posts.Post'),
        ),
    ]