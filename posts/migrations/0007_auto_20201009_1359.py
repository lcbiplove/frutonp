# Generated by Django 3.0.5 on 2020-10-09 08:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0006_remove_post_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='foodType',
            field=models.CharField(choices=[('bitter-gourd_NE_Bitter Gourd', 'Bitter Gourd'), ('cabbage_NE_Cabbage', 'Cabbage'), ('cauliflower_NE_Cauliflower', 'Cauliflower'), ('ladies-finger_NE_Ladies Finger', 'Ladies Finger'), ('pumpkin_NE_Pumpkin', 'Pumpkin'), ('apple_NE_Apple', 'Apple'), ('apple_NE_Banana', 'Banana'), ('apple_NE_Litchi', 'Litchi'), ('apple_NE_Mango', 'Mango'), ('apple_NE_Orange', 'Orange')], max_length=50, verbose_name='Food Type'),
        ),
    ]
