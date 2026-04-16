from django.urls import path
from . import views


urlpatterns = [
    path('', views.login_page, name='login_page'),
    path('signup/',views.signup_view, name='signup'),
    path('basic_list', views.basic_list, name='basic_list'),
    path('manage_account/<int:pk>', views.manage_account, name='manage_account'),
    path('change_password/<int:pk>/', views.change_password, name='change_password'),
    path('delete_account/<int:pk>/', views.delete_account, name='delete_account'),
    path('logout/', views.logout_view, name='logout'),
    path('add_menu', views.add_menu, name='add_menu'),
    path('view_detail/<int:pk>/', views.view_detail, name='view_detail'),
    path('delete_dish/<int:pk>/', views.delete_dish, name='delete_dish'),
    path('update_dish/<int:pk>/', views.update_dish, name='update_dish'),
]