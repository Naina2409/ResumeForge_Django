import re
from pathlib import Path
from ml_engine.scoring import load_artifact, score_pair

_ARTIFACT = None

def get_artifact():
    global _ARTIFACT
    if _ARTIFACT is None:
        _ARTIFACT = load_artifact()
    return _ARTIFACT

def _tokens(text):
    return set(re.findall(r"[a-zA-Z][a-zA-Z+#.]{2,}", (text or "").lower()))

def analyze_resume(resume_text, job_text):
    if not resume_text.strip() or not job_text.strip():
        raise ValueError("Both resume text and job description are required.")
    result = score_pair(resume_text, job_text, get_artifact())
    resume_tokens, job_tokens = _tokens(resume_text), _tokens(job_text)
    # Show the most relevant JD terms that are present/missing; this is a transparent
    # keyword insight, separate from the trained model's probability score.
    candidates = sorted(job_tokens, key=lambda term: (len(term), term), reverse=True)
    candidates = [term for term in candidates if term not in {"years", "year", "work", "team", "role", "job", "skills", "skill"}][:40]
    matched = sorted(set(candidates) & resume_tokens)
    missing = sorted(set(candidates) - resume_tokens)
    return {
        "score": float(result["score"]),
        "label": result["label"],
        "features": result["features"],
        "matched_keywords": matched[:15],
        "missing_keywords": missing[:15],
    }
