# Generated by Django 3.0.5 on 2020-10-09 14:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0007_auto_20201009_1359'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='foodType',
            field=models.CharField(choices=[('bitter-gourd_NE_करेला', 'Bitter Gourd'), ('cabbage_NE_बन्दागोभी', 'Cabbage'), ('cauliflower_NE_गोभी, काउली', 'Cauliflower'), ('ladies-finger_NE_चिप्लिभिन्डी', 'Ladies Finger'), ('pumpkin_NE_फर्सी', 'Pumpkin'), ('apple_NE_स्याऊ', 'Apple'), ('banana_NE_केरा', 'Banana'), ('litchi_NE_लिची', 'Litchi'), ('mango_NE_आँप', 'Mango'), ('orange_NE_सुन्तला', 'Orange')], max_length=50, verbose_name='Food Type'),
        ),
    ]