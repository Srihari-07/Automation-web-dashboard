 # SQLAlchemy class is the core component to create an DB instance which builds the connection between the Flask app and Database.
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# We initialize the 'db' object here, but don't attach it to an app yet.
# This makes it easy for other files to import.
db = SQLAlchemy() # The instance of the Database using SQLAlchemy Class

# This class is extending the db.Model class which makes this Class capable of modeling a table inside the DB
class AutomationTask(db.Model): #db.Model is a sub class coming from SQLAlchemy class
    __tablename__ = 'automation_tasks'

    # 1. Identity
    id = db.Column(db.Integer, primary_key=True)
    
    # 2. Description of the work
    task_type = db.Column(db.String(50), nullable=False) # e.g., 'organize_downloads'
    
    # 3. The "State Store" fields (Replacing your TASKS dictionary)
    status = db.Column(db.String(20), default='pending') # pending, running, completed, failed
    progress = db.Column(db.Integer, default=0)         # 0 to 100
    
    # 4. Metadata
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    def to_dict(self):
        """Helper to convert the database object into a JSON-friendly dictionary for your Status API."""
        return {
            "id": self.id,
            "task_type": self.task_type,
            "status": self.status,
            "progress": self.progress,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }
