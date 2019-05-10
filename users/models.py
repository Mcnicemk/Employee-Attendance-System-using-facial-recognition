from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from datetime import datetime


class AdminProfile(models.Model):
    user = models.OneToOneField(User, on_delete=None, primary_key=True)
    description = models.CharField(max_length=100, default=' ')
    city = models.CharField(max_length=20, default="")
    phone = models.IntegerField(default=0)
    head_shot = models.ImageField(upload_to='profil_images/admin', blank=True)

    class Meta:
        ordering = ["user"]

    def __str__(self):
        return self.user.username


def create_profile(**kwargs):
    if kwargs['created']:
        user_profile = AdminProfile.objects.get_or_create(user=kwargs['instance'])


post_save.connect(create_profile, sender=User)


class StudentsData(models.Model):
    reg_no = models.CharField(max_length=20, default="", primary_key=True)
    name = models.CharField(max_length=50, default=' ')
    surname = models.CharField(max_length=50, default="")
    email = models.CharField(max_length=500, default=' ')
    phone = models.IntegerField(default=0)
    country = models.CharField(max_length=50, default=' ')
    address = models.CharField(max_length=100, default=' ')
    picture = models.ImageField(upload_to='profil_images/students', blank=True)


class LecturerData(models.Model):
    l_id = models.CharField(max_length=20, default="", primary_key=True)
    name = models.CharField(max_length=50, default=' ')
    surname = models.CharField(max_length=50, default="")
    email = models.CharField(max_length=500, default=' ')
    phone = models.IntegerField(default=0)
    country = models.CharField(max_length=50, default=' ')
    address = models.CharField(max_length=100, default=' ')
    faculty = models.CharField(max_length=200, default="")
    picture = models.ImageField(upload_to='profil_images/lecturer', blank=True)


class Courses(models.Model):
    course_id = models.CharField(max_length=20, default="", primary_key=True)
    department_id = models.CharField(max_length=50, default=' ')
    course_name = models.CharField(max_length=50, default="")
    semester = models.CharField(max_length=50, default=' ')
    year = models.CharField(max_length=50, default=' ')


class LecturerAttendance(models.Model):
    a_id = models.CharField(max_length=20, default="", primary_key=True)
    l_id = models.CharField(max_length=50, default=' ')
    day = models.CharField(max_length=100, default=datetime.now, blank=True)
    time_in = models.CharField(max_length=100, default=datetime.now, blank=True)
    time_out = models.CharField(max_length=100, default=datetime.now, blank=True)
    status = models.CharField(max_length=50, default=' ')


class Faculty(models.Model):
    faculty_id = models.CharField(max_length=20, default="", primary_key=True)
    faculty_name = models.CharField(max_length=100, default="")


class Department(models.Model):
    department_id = models.CharField(max_length=20, default="", primary_key=True)
    faculty_id = models.CharField(max_length=20, default="")
    department_name = models.CharField(max_length=100, default="")


class Time_frame(models.Model):
    t_id = models.CharField(max_length=20, default="1", primary_key=True)
    timeframe = models.CharField(max_length=100, default="120", )
