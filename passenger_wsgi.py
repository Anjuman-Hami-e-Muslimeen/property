import sys
import os

# Add the project directory to the Python path if not already present
project_home = os.path.dirname(os.path.abspath(__file__))
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Set the environment to production (optional, can also be set in .env)
os.environ.setdefault('FLASK_ENV', 'production')

# Import the Flask app
from app import app as application

if __name__ == "__main__":
    application.run()