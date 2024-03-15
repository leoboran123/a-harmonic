
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [

    path('login/', views.userLogin, name="userLogin"),
    path('register/', views.userRegister, name="userRegister"),
    path('logout/', views.userLogout, name="userLogout"),
    

    
    path('myaccount/', views.userAccount, name="userAccount"),
    path('myprofile/', views.userProfileUpdate, name="userProfile"),
    path('userupdate/', views.userUpdate, name="updateUser"),
    path('myorders/', views.userOrders, name="userOrders"),
    path('orderproducts/', views.userOrderProducts, name="userOrderProducts"),
    path('mycoupons/', views.userCoupons, name="userCoupons"),

    path('changepassword/', views.changeUserPassword, name="changePassword"),



    path('mycart/', views.userCart, name="userCart"),



]
