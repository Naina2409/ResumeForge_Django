from pathlib import Path
from django import forms
from .models import Resume

MAX_FILE_SIZE = 10 * 1024 * 1024

class ResumeUploadForm(forms.ModelForm):
    class Meta:
        model = Resume
        fields = ["title", "file"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "field", "placeholder": "e.g. Software Developer Resume"}),
            "file": forms.ClearableFileInput(attrs={"class": "file-field", "accept": ".pdf,.docx"}),
        }

    def clean_file(self):
        uploaded = self.cleaned_data["file"]
        ext = Path(uploaded.name).suffix.lower()
        if ext not in {".pdf", ".docx"}:
            raise forms.ValidationError("Please upload a PDF or DOCX file.")
        if uploaded.size > MAX_FILE_SIZE:
            raise forms.ValidationError("File size must be 10 MB or less.")
        return uploaded
