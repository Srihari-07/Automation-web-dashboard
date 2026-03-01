import threading # Using for creating a Background Job
from models import db, AutomationTask # Database Object and Table Model
from worker import downloadsOrganizer # Worker function to do the real work

from run import create_app  # Import the function which returns the main flask object
app = create_app() # Flask Object

def createJob():
    # create new task in DB
    new_task = AutomationTask(task_type="organize_downloads", status="pending")
    db.session.add(new_task)
    db.session.commit()
    
    thread = threading.Thread(target=downloadsOrganizer, args=(new_task.id,))
    thread.start()

    return new_task

def getTaskStatus(task_id):
	task = AutomationTask.query.get(task_id) # Getting the task record from the DB
	if not task:
		return jsonify({"error": "Task not found"}), 404
	return jsonify(task.to_dict())

def getTask(task_id):
	with app.app_context():
		currentTask = AutomationTask.query.get(task_id)
		if not currentTask:
			currentTask.status = "failed"
			db.session.commit()
		return currentTask


def updateDB_status(task_id, task_status):
	# The worker MUST work inside the "app_context" to talk to the DB
	with app.app_context():


def updateDB_progress(task_id, task_progress):
	with app.app_context():

