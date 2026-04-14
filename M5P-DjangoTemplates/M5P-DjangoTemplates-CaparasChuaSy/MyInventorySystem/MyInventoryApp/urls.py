from django.urls import path
from . import views


urlpatterns = [
    path('', views.login_view, name='login_page'),
    path('signup/',views.signup_view, name='signup'),
    path('basic_list/<int:pk>/', views.basic_list, name='basic_list'),
    path('manage_account/<int:pk>', views.manage_account, name='manage_account'),
    path('change_password/<int:pk>/', views.change_password, name='change_password'),
    path('delete_account/<int:pk>/', views.delete_account, name='delete_account'),
    path('logout/', views.logout_view, name='logout'),
    path('view_bottles/', views.view_bottles, name='view_bottles'),
    path('view_bottle_details/<int:pk>/', views.view_bottle_details, name='view_bottle_details'),
    path('delete_bottle/<int:pk>/', views.delete_bottle, name='delete_bottle'),
    path('add_bottle/', views.add_bottle, name='add_bottle'),
    path('view_supplier/', views.view_supplier, name='view_supplier'),
]