from django.contrib import admin
from .models import AdminProfile, StudentsData, LecturerData, Courses, Faculty, Department, LecturerAttendance


# Register your models here.

admin.site.register(AdminProfile)
admin.site.register(StudentsData)
admin.site.register(LecturerData)
admin.site.register(Courses)
admin.site.register(Faculty)
admin.site.register(Department)
admin.site.register(LecturerAttendance)

