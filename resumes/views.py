from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.http import FileResponse
from .forms import ResumeUploadForm
from .models import Resume
from .services import extract_resume_text

@login_required
def upload_resume(request):
    form = ResumeUploadForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        resume = form.save(commit=False)
        resume.user = request.user
        resume.save()
        try:
            resume.extracted_text = extract_resume_text(resume.file.path)
            resume.save(update_fields=["extracted_text"])
        except Exception as exc:
            resume.file.delete(save=False)
            resume.delete()
            messages.error(request, str(exc))
            return render(request, "resumes/upload.html", {"form": form})
        messages.success(request, "Resume uploaded and text extracted successfully.")
        return redirect("dashboard")
    return render(request, "resumes/upload.html", {"form": form})

@login_required
def resume_detail(request, pk):
    resume = get_object_or_404(Resume, pk=pk, user=request.user)
    return render(request, "resumes/detail.html", {"resume": resume})

@login_required
def delete_resume(request, pk):
    resume = get_object_or_404(Resume, pk=pk, user=request.user)
    if request.method == "POST":
        resume.file.delete(save=False)
        resume.delete()
        messages.success(request, "Resume deleted.")
    return redirect("dashboard")

@login_required
def download_resume(request, pk):
    resume = get_object_or_404(Resume, pk=pk, user=request.user)
    return FileResponse(resume.file.open("rb"), as_attachment=True, filename=resume.file.name.split("/")[-1])
