"""
Backend application package initialization
"""
from app.database import init_db

__version__ = "1.0.0"
__author__ = "OpenAffi Team"

# Initialize database on import
try:
    init_db()
except Exception:
    pass  # Database may already be initialized
