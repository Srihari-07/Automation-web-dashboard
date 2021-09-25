import threading # Using for creating a Background Job
from models import db, AutomationTask # Database Object and Table Model
from worker import downloadsOrganizer # Worker function to do the real work

from flask import current_app  # function which returns the main flask object instead of creating a new one 

def createJob():
    # create new task in DB
    app = current_app._get_current_object()

    new_task = AutomationTask(task_type="organize_downloads", status="pending")
    db.session.add(new_task)
    db.session.commit()
    
    thread = threading.Thread(
    	target=downloadsOrganizer,
    	args=(app, new_task.id ,updateDB_status, updateDB_progress)
    	)
    thread.start()

    return new_task

def getTaskStatus(task_id):
	app = current_app._get_current_object()
	with app.app_context():
		task = AutomationTask.query.get(task_id)
		if task:
			return {"status":task.status,
					"progress":task.progress
			}

# This function is the 'tool' we inject into the worker
def updateDB_status(app,task_id, task_status):
	with app.app_context():
		task = AutomationTask.query.get(task_id)
		if task:
			task.status = task_status
			db.session.commit()

def updateDB_progress(app,task_id, task_progress):
	with app.app_context():
		task = AutomationTask.query.get(task_id)
		if task:
			task.progress = task_progress
			db.session.commit()
	
