from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from resumes.models import Resume
from analysis_app.models import JobDescription, Analysis

def home(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    return render(request, "home.html")

def register(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    form = UserCreationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, "Your ResumeForge account is ready.")
        return redirect("dashboard")
    return render(request, "registration/register.html", {"form": form})

@login_required
def dashboard(request):
    resumes = Resume.objects.filter(user=request.user).order_by("-uploaded_at")
    jobs = JobDescription.objects.filter(user=request.user).order_by("-created_at")
    analyses = Analysis.objects.filter(user=request.user).select_related("resume", "job_description").order_by("-created_at")[:5]
    total_analyses = Analysis.objects.filter(user=request.user).count()
    average_score = Analysis.objects.filter(user=request.user).values_list("score", flat=True)
    scores = list(average_score)
    avg = round(sum(scores) / len(scores) * 100) if scores else 0
    return render(request, "dashboard.html", {
        "resumes": resumes, "jobs": jobs, "analyses": analyses,
        "total_analyses": total_analyses, "average_score": avg,
    })
