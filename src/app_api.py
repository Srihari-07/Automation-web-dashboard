from flask import Blueprint, jsonify, request
from services.job_manager import createJob, getTaskStatus

api_bp = Blueprint("main", __name__)

# Status API
@api_bp.route("/status/<int:task_id>", methods=["GET"])
def get_status(task_id):
    id_status = getTaskStatus(task_id)
	return id_status

# Start API:
@api_bp.route("/downloads_Organizer/start", methods=["POST"])
def start_download_organizer():
    new_task = createJob()
    return jsonify({"task_id": new_task.id, "message": "Automation started"}),200





	