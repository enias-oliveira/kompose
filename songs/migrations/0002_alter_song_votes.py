# Generated by Django 3.2 on 2021-05-30 23:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('songs', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='song',
            name='votes',
            field=models.IntegerField(default=1),
        ),
    ]