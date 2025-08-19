from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('add/', views.add_task, name='add_task'),
    path('toggle/<int:pk>/', views.toggle_task, name='toggle_task'),
    path('delete/<int:pk>/', views.delete_task, name='delete_task'),
    path('edit-inline/<int:pk>/', views.edit_task_inline, name='edit_task_inline'),
    path('search/', views.search_tasks, name='search_tasks'),
]
