from django.contrib import admin
from django.urls import path, include
from core import views as core_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", core_views.home, name="home"),
    path("accounts/", include("django.contrib.auth.urls")),
    path("accounts/register/", core_views.register, name="register"),
    path("dashboard/", core_views.dashboard, name="dashboard"),
    path("resumes/", include("resumes.urls")),
    path("analysis/", include("analysis_app.urls")),
]
