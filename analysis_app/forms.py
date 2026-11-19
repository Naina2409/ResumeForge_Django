from django import forms
from .models import JobDescription

class JobDescriptionForm(forms.ModelForm):
    class Meta:
        model = JobDescription
        fields = ["title", "company", "description"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "field", "placeholder": "e.g. Python Developer"}),
            "company": forms.TextInput(attrs={"class": "field", "placeholder": "Company name (optional)"}),
            "description": forms.Textarea(attrs={"class": "field textarea", "rows": 9, "placeholder": "Paste the complete job description here..."}),
        }
