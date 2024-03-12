
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [

    path('addToCart/<int:id>/', views.addProductToCart, name="addToCart"),
    path('deleteFromCart/<int:id>/', views.deleteFromCart, name="deleteFromCart"),
    path('lessQuantityCart/<int:id>/', views.lessQuantityCart, name="lessQuantityCart"),
    path('moreQuantityCart/<int:id>/', views.moreQuantityCart, name="moreQuantityCart"),




]
