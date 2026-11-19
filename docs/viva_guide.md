# ResumeForge — quick viva guide

## 30-second introduction

ResumeForge is a Django-based resume-to-job matching platform. A user uploads a PDF or DOCX resume, saves a job description, and runs an analysis. Django handles authentication, file uploads, validation, database operations and result pages. The supplied trained TF-IDF/XGBoost model evaluates textual alignment and returns a fit score and label. The application stores reports so the user can review previous comparisons.

## Explain the workflow

- Registration and login use Django's built-in authentication.
- Resume upload is handled by a Django ModelForm and FileField.
- `resumes/services.py` extracts text from PDF or DOCX.
- Job descriptions and analysis reports are stored as Django models.
- The analysis service calls the original model scoring code.
- The result page shows the score, fit label, model feature signals, and a separate keyword preview.

## Course concepts to point at in the code

| Concept | File |
|---|---|
| Project URL routing | `config/urls.py` |
| App URL routing | `resumes/urls.py`, `analysis_app/urls.py` |
| Views | Each app's `views.py` |
| Models | `resumes/models.py`, `analysis_app/models.py` |
| Forms and validation | `resumes/forms.py`, `analysis_app/forms.py` |
| ORM | `core/views.py`, `analysis_app/views.py` |
| Authentication | `django.contrib.auth` decorators and built-in views |
| Templates | `templates/` |
| Template inheritance | `templates/base.html` |
| Static files | `static/css/style.css`, `static/js/app.js` |
| Media uploads | `MEDIA_ROOT` and `Resume.file` |
| Admin | Each app's `admin.py` |
| Migrations | `python manage.py makemigrations` and `migrate` |

## Explain the model carefully

The original service computes eight features: TF-IDF cosine similarity, keyword overlap, job-description coverage, experience gap, missing-experience indicator, resume word count, job-description word count and their length ratio. The trained classifier returns a probability. The original thresholds map the probability to `Good Fit`, `Potential Fit` or `No Fit`.

The match score is not a hiring probability. It is a model estimate of resume/job-description fit. Keyword chips are an additional, rule-based explanation aid and not the classifier's prediction.

## Demo sequence

1. Register a test user.
2. Upload a text-based PDF or DOCX resume.
3. Create a job description.
4. Run the analysis.
5. Explain the score and the feature values.
6. Open history and show that the analysis was saved.
7. Open `/admin/` to demonstrate Django's admin site.
