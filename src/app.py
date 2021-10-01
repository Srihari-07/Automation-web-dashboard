from flask import Flask, render_template, jsonify
from AutomationEngine.downloadsOrganizer import organize_Downloads

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
@app.route("/api/downloads_Organizer/run", methods=["POST"])
def run_organizer():

    results = organize_Downloads()
    if not results:
    	return jsonify({
    	   "status": "failed",
           "message": "Can't access the Download's Folder"
    	}),404

    return jsonify({
           "status": "success",
           "message": "Files organized successfully",
           "result": results
    	}), 200



if __name__ == '__main__':
	app.run(debug=True)



