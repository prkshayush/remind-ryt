from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logOutUser, name='logout'),
    path('register/', views.registerPage, name='register'),
    path('', views.home, name='home'),
    path('group/<str:key>/', views.group, name='group'),
    path('create-group/', views.createGroup, name='createGroup'),
    path('join-group/<str:key>', views.joinGroup, name='join_group'),
]