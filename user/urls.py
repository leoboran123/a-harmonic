
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [

    path('login/', views.userLogin, name="userLogin"),
    path('register/', views.userRegister, name="userRegister"),
    path('logout/', views.userLogout, name="userLogout"),
    

    
    path('myaccount/', views.userAccount, name="userAccount"),
    path('mycart/', views.userCart, name="userCart"),



]