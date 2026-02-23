from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('chat/', views.chat, name='chat'),
    path('schedule/', views.schedule, name='schedule'),
    path('delete/<int:id>/', views.delete_activity, name='delete_activity'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    path('edit/<int:id>/', views.edit_activity, name='edit_activity'),
]