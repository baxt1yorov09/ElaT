from __future__ import annotations

# Expose the Celery app so shared_task can autodiscover it when Django starts.
from .celery import app as celery_app

__all__ = ("celery_app",)
