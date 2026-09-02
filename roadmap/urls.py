from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='roadmap_home'),
    path('generate/', views.generate_roadmap_view, name='generate_roadmap'),
    path('detail/<int:pk>/', views.roadmap_detail_view, name='roadmap_detail'),
    path('daily/<int:pk>/', views.daily_guidance_view, name='roadmap_daily_guidance'),
    path('progress/<int:pk>/', views.progress_view, name='roadmap_progress'),
    path('history/', views.history_view, name='roadmap_history'),
    path('roadmap/<int:pk>/delete/', views.delete_roadmap_view, name='delete_roadmap'),
    path('task/<int:pk>/toggle/', views.toggle_task_view, name='toggle_task'),
]
