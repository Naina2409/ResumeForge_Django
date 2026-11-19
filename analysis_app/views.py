from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from resumes.models import Resume
from .forms import JobDescriptionForm
from .models import JobDescription, Analysis
from .services import analyze_resume

@login_required
def create_job(request):
    form = JobDescriptionForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        job = form.save(commit=False)
        job.user = request.user
        job.save()
        messages.success(request, "Job description saved. You can now run an analysis.")
        return redirect("analysis_run_for_job", job_id=job.pk)
    return render(request, "analysis_app/job_form.html", {"form": form})

@login_required
def run_analysis(request, job_id=None):
    jobs = JobDescription.objects.filter(user=request.user).order_by("-created_at")
    resumes = Resume.objects.filter(user=request.user).order_by("-uploaded_at")
    if request.method == "POST":
        resume = get_object_or_404(Resume, pk=request.POST.get("resume"), user=request.user)
        job = get_object_or_404(JobDescription, pk=request.POST.get("job"), user=request.user)
        try:
            result = analyze_resume(resume.extracted_text, job.description)
        except Exception as exc:
            messages.error(request, f"Analysis could not be completed: {exc}")
            return redirect("analysis_run")
        analysis = Analysis.objects.create(
            user=request.user, resume=resume, job_description=job,
            score=result["score"], label=result["label"], features=result["features"],
            matched_keywords=result["matched_keywords"], missing_keywords=result["missing_keywords"],
        )
        return redirect("analysis_detail", pk=analysis.pk)
    selected_job = get_object_or_404(JobDescription, pk=job_id, user=request.user) if job_id else None
    return render(request, "analysis_app/run.html", {
        "jobs": jobs, "resumes": resumes, "selected_job": selected_job,
    })

@login_required
def analysis_detail(request, pk):
    analysis = get_object_or_404(
        Analysis.objects.select_related("resume", "job_description"),
        pk=pk, user=request.user,
    )
    return render(request, "analysis_app/result.html", {
        "analysis": analysis,
        "score_percent": round(analysis.score * 100),
    })

@login_required
def analysis_history(request):
    analyses = Analysis.objects.filter(user=request.user).select_related("resume", "job_description")
    return render(request, "analysis_app/history.html", {"analyses": analyses})


@login_required
def edit_job(request, pk):
    job = get_object_or_404(JobDescription, pk=pk, user=request.user)
    form = JobDescriptionForm(request.POST or None, instance=job)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Job description updated.")
        return redirect("dashboard")
    return render(request, "analysis_app/job_form.html", {"form": form, "editing": True})

@login_required
def delete_job(request, pk):
    job = get_object_or_404(JobDescription, pk=pk, user=request.user)
    if request.method == "POST":
        job.delete()
        messages.success(request, "Job description and its analyses were deleted.")
    return redirect("dashboard")
