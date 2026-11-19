from django.urls import path
from . import views
urlpatterns = [
    path("jobs/new/", views.create_job, name="job_create"),
    path("run/", views.run_analysis, name="analysis_run"),
    path("run/<int:job_id>/", views.run_analysis, name="analysis_run_for_job"),
    path("history/", views.analysis_history, name="analysis_history"),
    path("<int:pk>/", views.analysis_detail, name="analysis_detail"),
    path("jobs/<int:pk>/edit/", views.edit_job, name="job_edit"),
    path("jobs/<int:pk>/delete/", views.delete_job, name="job_delete"),
]
