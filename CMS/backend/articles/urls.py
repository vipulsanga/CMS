from django.urls import path
from . import views

urlpatterns = [
    path('', views.frontend, name='frontend'),
    path('admin/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/login/', views.admin_login, name='admin_login'),
    path('admin/logout/', views.admin_logout, name='admin_logout'),
    path('health/', views.health_check, name='health_check'),
    path('api/articles/', views.api_article_list, name='api_article_list'),
    path('api/articles/<str:pk>/', views.api_article_detail, name='api_article_detail'),
    path('articles/<int:pk>/', views.frontend, name='article_detail'),
]
