# Generated by Django 3.1.4 on 2021-01-30 02:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movieist', '0005_auto_20210125_1222'),
    ]

    operations = [
        migrations.AlterField(
            model_name='follow',
            name='follower',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='follow',
            name='following',
            field=models.IntegerField(null=True),
        ),
    ]