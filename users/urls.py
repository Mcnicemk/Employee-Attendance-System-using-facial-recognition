from django.urls import path
from . import views
from django.conf.urls import url, include
from django.contrib import admin


urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.create, name='create'),
    path('lec_create/', views.lec_create, name='lec_create'),
    path('caption/', views.caption, name='caption'),
    path('recognition/', views.recog, name='recog'),
    path('train/', views.train, name='train'),
    path('email/', views.email, name='email'),
    path('csv/', views.export_users_csv, name='csv'),
    path('excel/', views.export_users_xls, name='excel'),
    path('graphs/', views.graphs, name='graphs'),
    path('timeframe/', views.timeframe, name='timeframe'),
]