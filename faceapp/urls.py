from django.urls import path
from .import views

urlpatterns = [
  path('',views.home, name='face-home'),
  path('attend/',views.attend_view, name='attend_view'),
  path('dashboard/',views.dashboard, name='dashboard')
]