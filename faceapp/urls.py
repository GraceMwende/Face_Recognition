from django.urls import path
from .import views

urlpatterns = [
  path('',views.attend_view, name='attend_view')
]