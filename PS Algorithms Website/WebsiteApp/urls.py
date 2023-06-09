from django.contrib import admin
from django.urls import path
from WebsiteApp import views

urlpatterns = [
    path('', views.home, name = 'Home Page'),
    path('about/', views.about, name='About Page'),
    path('SRTF/', views.SRTF, name='SRTF Page'),
    path('done', views.SRTF, name='SRTF Output')
]