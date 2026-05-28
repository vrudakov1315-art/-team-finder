from django.urls import path

from . import views

app_name = 'users'

urlpatterns = [
    path('register/', views.user_register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('list/', views.user_list, name='list'),
    path('edit-profile/', views.edit_profile, name='edit-profile'),
    path('change-password/', views.change_password, name='change-password'),
    path('<int:pk>/', views.user_detail, name='detail'),
]
