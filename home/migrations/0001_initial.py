# Generated by Django 3.0.5 on 2020-06-30 16:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('posts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='NotifClick',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('new_count', models.PositiveIntegerField(default=0, verbose_name='New notifications')),
                ('myuser', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='notif_click', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Notif',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seen', models.BooleanField(default=False)),
                ('received_at', models.DateTimeField(auto_now=True, verbose_name='Received At')),
                ('comment', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='posts.Comment')),
                ('notif_click', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.NotifClick')),
                ('post', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='posts.Post')),
                ('reply', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='posts.Reply')),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
