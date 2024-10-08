from django.urls import path
from .import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='index'),
    path('add', views.add, name='add'),
    path('update/<int:todo_id>/', views.update, name='update'),
    path('delete/<int:todo_id>/', views.delete, name='delete'),
    path('calendar/', views.calendar_view, name='calendar'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('register/', views.register, name='register'),
    path('statistics/', views.statistics, name='statistics'),
    path('edit_ajax/', views.edit_ajax, name='edit_ajax'),  # Новый путь для обработки AJAX-запросов
]