from flask import Blueprint, jsonify, request
from models import db, AutomationTask # Database Table
import threading
from worker import downloadsOrganizer
from run import app

api_bp = Blueprint("main", __name__)

# Status API
@api_bp.route("/status/<int:task_id>", methods=["GET"])
def get_status(task_id):
	task = AutomationTask.query.get(task_id) # Getting
    if not task:
        return jsonify({"error": "Task not found"}), 404
    return jsonify(task.to_dict())


# Start API:
@api_bp.route("/downloads_Organizer/start", methods=["POST"])
def start_download_organizer():
	# Logic to create task in DB
    new_task = AutomationTask(task_type="organize_downloads", status="pending")
    db.session.add(new_task)
    db.session.commit()
    
    thread = threading.Thread(target=downloadsOrganizer, args=(new_task.id,))
    thread.start()

    return jsonify({"task_id": new_task.id, "message": "Automation started"}),200





	