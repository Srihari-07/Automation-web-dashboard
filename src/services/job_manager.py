import threading # Using for creating a Background Job
from models import db, AutomationTask # Database Object and Table Model
from worker import downloadsOrganizer # Worker function to do the real work

from flask import current_app  # function which returns the main flask object instead of creating a new one 

STATUS_PENDING = "pending"
STATUS_RUNNING = "running"
STATUS_COMPLETED = "completed"
STATUS_FAILED = "failed"

# State Machine : It's a Validation layer to validate the State Transition of a task
valid_states = {
	"pending" : ["running"],
	"running" : ["completed","failed"],
	"completed": [],
	"failed":[]
}

def transition_status(task, new_status):
	current_status = task.status
	allowed_status = valid_states.get(current_status, [])
	if new_status not in allowed_status:
		raise ValueError(
			f"Invalid status transition: {current_status} → {new_status}"
		)
	task.status = new_status


def createJob(taskType):
    # create new task in DB
    app = current_app._get_current_object()

    new_task = AutomationTask(task_type=taskType, status=STATUS_PENDING)
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
		return {"error": "Task not found"}

# This function is the 'tool' we inject into the worker
def updateDB_status(app,task_id, task_status):
	with app.app_context():
		task = AutomationTask.query.get(task_id)
		if task:
			try:
				transition_status(task, task_status) # Status Validation Layer
				db.session.commit()
			except ValueError as e:
				current_app.logger.error(str(e))


def updateDB_progress(app,task_id, task_progress):
	with app.app_context():
		task = AutomationTask.query.get(task_id)
		if task:
			task.progress = task_progress
			db.session.commit()
	
