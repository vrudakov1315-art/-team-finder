from django.urls import path
from . import views

app_name = 'projects'

urlpatterns = [
    path('list/', views.project_list, name='project_list'),
    path('create-project/', views.project_create, name='project_create'),
    path('favorites/', views.favorite_projects, name='favorite_projects'),
    path('<int:pk>/', views.project_detail, name='project_detail'),
    path('<int:pk>/edit/', views.project_edit, name='project_edit'),
    path('<int:pk>/complete/', views.project_complete, name='project_complete'),
    path('<int:pk>/toggle-participate/', views.toggle_participate, name='toggle_participate'),
    path('<int:pk>/toggle-favorite/', views.toggle_favorite, name='toggle_favorite'),
]
