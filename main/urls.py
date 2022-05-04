from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('home/', views.home, name='home'),
    path('fee/<int:pk>', views.fee, name='fee'),
    path('search/', views.search, name='search'),
    path('addcustomer/', views.addcustomer, name='addcustomer'),
    path('print/<int:pk>', views.print, name='print'),
    path('delete/<int:pk>', views.delete, name='delete'),
    path('edit_customer/<int:pk>', views.edit_customer, name='edit_customer'),
    path('show_subusers/', views.show_subusers, name='show_subusers'),
    path('add_subusers/', views.add_subusers, name='add_subusers'),
    path('report/', views.generatereport, name='report'),
    path('add-details/', views.shopdetails, name='add-details'),
    path('edit-details/<int:pk>', views.edit_shopdetails, name='edit-details'),
    path('details/', views.show_details, name='details'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

]
