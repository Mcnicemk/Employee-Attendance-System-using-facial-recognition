from django.shortcuts import render
from users.models import StudentsData, LecturerData, Faculty, LecturerAttendance
import os
import datetime


# Create your views here.
def login(request):
    return render(request, "registration/login.html", {})


def home(request):
    stu_count = StudentsData.objects.all().count()
    lec_count = LecturerData.objects.all().count()
    last_train = Faculty.objects.all()
    return render(request, "home.html", {'stu_count': stu_count, 'lec_count': lec_count, 'last_train': last_train})


def addstudent(request):
    return render(request, 'addstudent.html', {})


def training(request):
    return render(request, 'training.html', {})


def studentdetails(request):
    stu_de = StudentsData.objects.all()

    return render(request, 'studentdetails.html', {'stu_de': stu_de})


def teacher(request):
    return render(request, 'teacher.html', {})


def clas(request):
    return render(request, 'clas.html', {})


def subject(request):
    return render(request, 'subject.html', {})


def classroutine(request):
    return render(request, 'classroutine.html', {})


def dattendance(request):
    return render(request, 'dattedance.html', {})


def lock_screen(request):
    return render(request, 'lock_screen.html', {})


def attendance_report(request):
    att_re = LecturerAttendance.objects.all()
    return render(request, 'attendance_report.html', {'att_re': att_re})


def addadmin(request):
    return render(request, 'addadmin.html', {})


def viewadmin(request):
    admin_de = StudentsData.objects.all()
    return render(request, 'viewadmin.html', {'admin_de':admin_de})


def profile(request):
    return render(request, 'profile.html', {})


def lecturerdetails(request):
    lec_de = LecturerData.objects.all()

    return render(request, 'lecturerdetails.html', {'lec_de': lec_de})
