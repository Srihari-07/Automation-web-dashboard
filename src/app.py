from flask import Flask, render_template, jsonify
from AutomationEngine.downloadsOrganizer import organize_Downloads

import uuid # For Unique task ID's
import threading # Worker to handle heavy work (For now)

taskId = str(uuid.uuid4()) # Unique Task ID
app = Flask(__name__)

# Front-End Routes
@app.route("/")
@app.route("/automation")
def home():
	return render_template("home.html")

@app.route("/automation/downloads_Organizer")
def downloadOrganizer():
	return render_template("downloads_Organizer.html")



# API Routes

# Source of Truth: stored information about a background job.
TASKS = {
	
}

# Status Route to get the Current Status of task: 
@app.route("/api/downloads_Organizer/status", methods=["POST"])
def get_status():
	return jsonify({
		"status" : 
		})

# Start Route API:
@app.route("/api/downloads_Organizer/start", methods=["POST"])
def start_download_organizer():
	global TASKS
	TASKS[taskId] = {
		"status":"running",
		"progress":0,
		"result":None,
		"error":None
	}

	thread = threading.Thread(target=run_downloads_script,args=(taskId))
	thread.start()

	return jsonify({
		"task_id" : taskId
		}),200
	

	
    

# Worker Function:
def run_downloads_script(taskid):
	try:
		TASKS["task_1"]["status"] = "running"
		results = organize_Downloads()
		TASKS["task_1"]["status"] = "completed"

		if not results:
			TASKS["task_1"]["status"] = "failed"
			return jsonify({
    	   		"status": "failed",
           		"message": "Can't access the Download's Folder"
    		}),404

		return jsonify({
           	"status": "success",
           	"message": "Files organized successfully",
           	"result": results
    	}), 200

	except Exception as e:
		TASKS["downloads_organizer"] = "failed"
		return jsonify({
			"status" : "failed",
			"message" : str(e)
			}),500




if __name__ == '__main__':
	app.run(debug=True)



