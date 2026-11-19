# ResumeForge — Django + ML Resume Match Platform

ResumeForge helps a job seeker compare a resume with a job description. It extracts text from PDF/DOCX resumes, runs the supplied trained ResumeForge TF-IDF/XGBoost model, displays the match label and score, surfaces keyword overlaps/gaps, and saves analysis history per user.

## What is included

- Django project with `core`, `resumes`, and `analysis_app` apps.
- Django built-in authentication (register, login, logout).
- Resume upload with PDF/DOCX validation and text extraction.
- Job-description CRUD basics and per-user ownership checks.
- Actual trained model artifact and scoring implementation from the supplied `resumeforge-ml-service` ZIP.
- Analysis result page with model features and keyword insights.
- Analysis history and Django admin.
- Responsive SaaS-style landing page and dashboard.

## Important model note

The ML service's `score` is a model probability used by its original `Good Fit`, `Potential Fit`, and `No Fit` thresholds. The UI expresses that number as a percentage for readability. It is a resume/job textual-fit estimate, **not** a probability of getting hired. The keyword chips are a separate transparent token-overlap preview, not a second trained classifier.

The model artifact was serialized with `numpy==2.0.2` and `scikit-learn==1.6.1`; keep these versions pinned. XGBoost CPU package is pinned to the original service's version.

## Windows setup (VS Code)

Open the `ResumeForge_Django` folder in VS Code. Copy `.env.example` to `.env`, update the secret key, then open Terminal → New Terminal (PowerShell or CMD).

### 1. Create and activate a virtual environment

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, use CMD instead:

```cmd
.venv\Scripts\activate.bat
```

### 2. Install dependencies

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Create database tables

```powershell
python manage.py makemigrations resumes analysis_app
python manage.py migrate
```

### 4. Create admin user (optional)

```powershell
python manage.py createsuperuser
```

### 5. Start the development server

```powershell
python manage.py runserver
```

Open http://127.0.0.1:8000/

## First-time demo flow

1. Register a new account.
2. Upload a text-based PDF or DOCX resume (maximum 10 MB).
3. Add a job description.
4. Run a match analysis.
5. Review the match score, original model label, feature signals, matched terms and potential keyword gaps.
6. Open Analysis history to revisit the saved report.
7. Visit `/admin/` with your superuser account to demonstrate Django admin.

## Django concepts demonstrated

| Course concept | Implementation |
|---|---|
| Project/app structure | `config`, `core`, `resumes`, `analysis_app` |
| URL routing | `config/urls.py` and app `urls.py` |
| Views | `views.py` in each app |
| Models | Resume, JobDescription, Analysis |
| Migrations | `makemigrations`, `migrate` |
| ORM | Per-user filtering, create, delete, related-object queries |
| Forms | ResumeUploadForm, JobDescriptionForm, UserCreationForm |
| Authentication | Django login/logout/register |
| Templates | Shared `base.html` and page templates |
| Static files | CSS and JavaScript in `static/` |
| Media files | Uploaded documents in `media/` |
| Admin | Model registration in `admin.py` |
| ML integration | `analysis_app/services.py` calls `ml_engine/scoring.py` |

## Project layout

```text
ResumeForge_Django/
├── manage.py
├── config/
├── core/
├── resumes/
├── analysis_app/
├── ml_engine/
│   ├── scoring.py
│   └── model/match_model.joblib
├── templates/
├── static/
├── media/
├── requirements.txt
└── README.md
```

## Production hardening before public deployment

This package is a local development/coursework starter. Before a public deployment:
- Set a strong `DJANGO_SECRET_KEY`, `DEBUG=False`, and production `ALLOWED_HOSTS`.
- Use PostgreSQL and a proper production WSGI/ASGI server.
- Put uploaded resumes in private object storage and serve them only after authorization; do not expose the development `media/` directory publicly.
- Add file malware scanning, rate limits, audit logging, backups, and a retention/deletion policy.
- Configure HTTPS, secure cookies, CSRF trusted origins, and monitoring.
- Consider moving model scoring back behind the original FastAPI `/score` API if the ML service needs independent scaling.

## Limitations / next milestones

- Local PDF text extraction works for text-based PDFs; scanned image PDFs need OCR.
- The original Next.js Gemini-powered resume parsing and tailored PDF generation are not silently replicated here. They can be added as an optional AI feature with a configured Gemini API key and a clear user review step.
- GitHub project import and Google OAuth from the original Next.js app are future enhancements, not included in this first Django conversion.
