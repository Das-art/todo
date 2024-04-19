# project/urls.py

from django.urls import path
from . import views

urlpatterns = [
     path('', views.project_list, name='project_list'),
     path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
   
    path('add/', views.project_add, name='project_add'),
    path('<int:project_id>/', views.project_detail, name='project_detail'),
    path('export-gist/', views.export_gist, name='export_gist'),
    path('<int:project_id>/edit/', views.project_edit, name='project_edit'),
    path('<int:project_id>/delete/', views.project_delete, name='project_delete'),
    path('<int:project_id>/task/add/', views.task_add, name='task_add'),
    path('<int:project_id>/task/<int:task_id>/edit/', views.task_edit, name='task_edit'),
    path('<int:project_id>/task/<int:task_id>/delete/', views.task_delete, name='task_delete'),
]
