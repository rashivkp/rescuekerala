from django.urls import path

from . import views

urlpatterns = [
    path('register/', views.proces_log, name='home'),
    path('add_volunteer/', views.create_volunteer, name='home'),
    path('approve_volunteer/', views.approve_volunteer, name='home'),
    path('view/<int:pk>/', views.view_request, name='view_request'),
]
