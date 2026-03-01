import os
from pathlib import Path

# Get the folder where this file lives
basedir = Path(__file__).resolve().parent

class Config:
    # Use an environment variable for the DB URI, or fall back to a local file
	SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
	'sqlite:///' + str(basedir / 'tasks.db')
    
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	SECRET_KEY = 'your-secret-key-here' # Important for later (sessions/security)
