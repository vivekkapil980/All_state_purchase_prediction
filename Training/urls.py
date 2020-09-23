from django.contrib import admin
from django.urls import path
from . import views

#to access links all over the html files
app_name="training"
urlpatterns = [
    #this end point has a form to allow user to submit for predicted insurance quote
    path('main/', views.Home_Page,name="main_page"),
    #navigates to about page which has details about the website
    path('about/', views.Test,name="test"),

    #navigates to analysis page where the demographics is shown clearly between
    #different variables
    path('analysis/', views.stack_chart,name="analysis"),

]
