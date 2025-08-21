import sys
import os

# Add the application directory to Python path
sys.path.insert(0, os.path.dirname(__file__))

from app import app

# Initialize database when the application starts
from app import init_db
init_db()

# WSGI callable object
application = app

if __name__ == "__main__":
    application.run()