# Generated by Django 2.1.7 on 2019-05-09 08:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_auto_20190509_1021'),
    ]

    operations = [
        migrations.AddField(
            model_name='time',
            name='t_id',
            field=models.CharField(default='1', max_length=20, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='time',
            name='timeframe',
            field=models.CharField(default='120', max_length=100),
        ),
    ]