from django.contrib import admin
from .models import JobDescription, Analysis
admin.site.register(JobDescription)
@admin.register(Analysis)
class AnalysisAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "resume", "job_description", "score", "label", "created_at")
    list_filter = ("label", "created_at")
