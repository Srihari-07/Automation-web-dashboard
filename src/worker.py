from run import create_app # Function handling the DB Configs and Object
from models import db, AutomationTask # For connecting Database to the worker

from AutomationEngine.downloadsOrganizer import organize_Downloads # Actual Automation Script

# Creating an app instance so the worker can use the DB settings
app = create_app()

def downloadsOrganizer(task_id):
    # The worker MUST work inside the "app_context" to talk to the DB
    with app.app_context():
        task = AutomationTask.query.get(task_id)
        if not task: return

        task.status = "running"
        db.session.commit()

        # --- Automation Logic here ---
        try:
			results = organize_Downloads() # Returns Dictionary of files moved and skipped
			
		except Exception as e:
			# Code here
        db.session.commit() # Save progress to SQLite

        task.status = "completed"
        task.progress = 100
        db.session.commit()




	