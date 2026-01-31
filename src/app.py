from flask import Flask, render_template, jsonify

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
@app.route("/api/downloads_Organizer")
def organizeDownloads():
	pass


if __name__ == '__main__':
	app.run(debug=True)



