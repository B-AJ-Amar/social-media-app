# Generated by Django 4.2.2 on 2023-07-03 21:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='photo',
            field=models.ImageField(default='user_photos/user_default.png', upload_to='user_photos/<function getusername at 0x0000029244166340>'),
        ),
    ]
