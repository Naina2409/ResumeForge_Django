# ML engine

This folder contains the scoring implementation and trained model artifact from the supplied ResumeForge ML service repository. The Django app calls `score_pair()` directly for a single-process local setup. The original FastAPI service can be deployed separately later if needed.

The model artifact was trained with scikit-learn 1.6.1 and numpy 2.0.2. Keep those versions pinned when loading the joblib artifact.
