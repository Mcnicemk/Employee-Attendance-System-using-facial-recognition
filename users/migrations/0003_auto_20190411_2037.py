# Generated by Django 2.1.7 on 2019-04-11 18:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_attendance'),
    ]

    operations = [
        migrations.CreateModel(
            name='LecturerAttendance',
            fields=[
                ('a_id', models.CharField(default='', max_length=20, primary_key=True, serialize=False)),
                ('l_id', models.CharField(default=' ', max_length=50)),
                ('date', models.CharField(default='', max_length=50)),
                ('status', models.CharField(default=' ', max_length=50)),
            ],
        ),
        migrations.DeleteModel(
            name='Attendance',
        ),
    ]