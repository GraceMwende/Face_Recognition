from django.urls import path
from .import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
  path('',views.home, name='face-home'),
  path('attend/',views.attend_view, name='attend_view'),
  path('dashboard/',views.dashboard, name='dashboard'),
  path('image_upload', views.upload_photos, name = 'image_upload'),
  path('create_user', views.create_user, name = 'create_user'),
  path('mark_attendance', views.face_attend_view,name='mark_attendance'),
  path('admin-reports/', views.generate_reports, name='admin-reports')
]
if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)