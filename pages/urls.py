from django.urls import path
from . import views


urlpatterns = [
    path('login/', views.login, name='login'),
    path('dashboard/', views.home, name='home'),
    path('addstudent/',views.addstudent,name='addstudent'),
    path('studentdetails/',views.studentdetails,name='studentdetails'),
    path('teacher/',views.teacher,name='teacher'),
    path('clas/',views.clas,name='clas'),
    path('subject/',views.subject,name='subject'),
    path('classroutine/',views.classroutine,name='classroutine'),
    path('dattendance/',views.dattendance,name='dattendance'),
    path('lock_screen/',views.lock_screen,name='lock_screen'),
    path('attendance_report/',views.attendance_report,name='attendance_report'),
    path('add_admin/',views.addadmin,name='addadmin'),
    path('profile/',views.profile,name='profile'),
    path('lecturer_details/',views.lecturerdetails,name='lecturerdetails'),
    path('training/',views.training,name='training'),
    path('view_admin/',views.viewadmin,name='viewadmin'),


]