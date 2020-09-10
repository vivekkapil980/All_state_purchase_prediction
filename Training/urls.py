from django.contrib import admin
from django.urls import path
from . import views

app_name="training"
urlpatterns = [
    path('', views.Home_Page, name="main_page"),
    path('Test/', views.Test, name="test"),
]
