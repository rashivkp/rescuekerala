from django.urls import path

from . import views

urlpatterns = [
    path('register/', views.proces_log, name='home'),
]
