from django.urls import path
from . import views

urlpatterns = [
    path('', views.habit_list, name='habit_list'),
    path('add/', views.add_habit, name='add_habit'),
    path('toggle/<int:pk>/', views.toggle_habit, name='toggle_habit'),
    path('delete/<int:pk>/', views.delete_habit, name='delete_habit'),
    path('history/<int:pk>/', views.habit_history, name='habit_history'),
]