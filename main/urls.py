from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('home/', views.home, name='home'),
    path('area/', views.area, name='area'),
    path('add_area/', views.add_area, name='add_area'),
    path('add_subarea/<int:pk>', views.add_subarea, name='add_subarea'),
    path('fee/<int:pk>', views.fee, name='fee'),
    path('edit-fee/<int:pk>', views.edit_fee, name='edit-fee'),
    path('search/', views.search, name='search'),
    path('addcustomer/', views.addcustomer, name='addcustomer'),
    path('print/<int:pk>', views.print, name='print'),
    path('show/<int:pk>', views.showprint, name='show'),
    path('delete/<int:pk>', views.delete, name='delete'),
    path('edit_customer/<int:pk>', views.edit_customer, name='edit_customer'),
    path('show_subusers/', views.show_subusers, name='show_subusers'),
    path('fee_paid/', views.fee_paid, name='fee_paid'),
    path('add_subusers/', views.add_subusers, name='add_subusers'),
    path('report/', views.generatereport, name='report'),
    path('monthly_report/', views.generatereport_month, name='monthly_report'),
    path('search-and-print/', views.search_and_print, name='search-and-print'),
    path('disabled_customer/', views.get_disabled, name='disabled_customer'),
    path('active_customer/', views.get_active, name='active_customer'),
    path('total_customer/', views.get_total, name='total_customer'),
    path('paid_customer/', views.get_paid, name='paid_customer'),
    path('notpaid_customer/', views.get_notpaid, name='notpaid_customer'),
    path('add-details/', views.shopdetails, name='add-details'),
    path('edit-details/<int:pk>', views.edit_shopdetails, name='edit-details'),
    path('details/', views.show_details, name='details'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

]
