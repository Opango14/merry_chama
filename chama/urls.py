from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('create-group/', views.create_group, name='create_group'),
    path('group/<int:pk>', views.group_detail, name='group_detail'),
    path('group/<int:group_id>/contribute/', views.record_contribution, name='record_contriution'),
    path('group/<int:group_id>/distributive-savings/', views.distributive_savings, name='distributive_savings'),
]