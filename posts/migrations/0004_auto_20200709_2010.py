# Generated by Django 3.0.5 on 2020-07-09 14:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0003_auto_20200703_1635'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='foodType',
            field=models.CharField(choices=[('apple', 'Apple'), ('banana', 'Banana'), ('litchi', 'Litchi'), ('mango', 'Mango'), ('orange', 'Orange'), ('bitter-gourd', 'Bitter Gourd'), ('cabbage', 'Cabbage'), ('cauliflower', 'Cauliflower'), ('ladies-finger', 'Ladies Finger'), ('pumpkin', 'Pumpkin')], max_length=50, verbose_name='Food Type'),
        ),
        migrations.AlterField(
            model_name='post',
            name='quantity',
            field=models.CharField(choices=[('kg', '1 kg'), ('250gm', '250 gm'), ('200gm', '200 gm'), ('500gm', '500 gm'), ('2kg', '2 kg'), ('5kg', '5 kg'), ('10kg', '10 kg'), ('25kg', '25 kg'), ('50kg', '50 kg'), ('quintal', '1 quintal')], max_length=30),
        ),
    ]
