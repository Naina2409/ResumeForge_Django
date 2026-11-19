from django.urls import path
from . import views
urlpatterns = [
    path("upload/", views.upload_resume, name="resume_upload"),
    path("<int:pk>/", views.resume_detail, name="resume_detail"),
    path("<int:pk>/download/", views.download_resume, name="resume_download"),
    path("<int:pk>/delete/", views.delete_resume, name="resume_delete"),
]
