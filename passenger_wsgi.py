import os, sys

# Point to your cPanel Python virtualenv interpreter
INTERP = os.path.expanduser("/home/anjumanedu/virtualenv/public_html/3.9/bin/python")
if sys.executable != INTERP:
    os.execl(INTERP, INTERP, *sys.argv)

# Ensure project root is on sys.path
PROJECT_ROOT = os.path.dirname(__file__)
sys.path.insert(0, PROJECT_ROOT)

# Optional: chdir to project root (helps template paths)
os.chdir(PROJECT_ROOT)

# Import the Flask app instance
from app_production import app as application