# Generated by Django 4.2.2 on 2023-07-08 14:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0004_post_is_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reaction',
            name='type',
            field=models.CharField(choices=[('like', 'like'), ('dislike', 'dislike')], max_length=8, null=True),
        ),
    ]