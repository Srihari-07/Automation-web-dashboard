from flask import Blueprint, request,render_template

# Blueprint Object
view_bp = Blueprint('view', __name__)

@view_bp.route("/")
@view_bp.route("/automation")
def home():
	return render_template("home.html")

@view_bp.route("/automation/downloads_Organizer")
def downloadOrganizer():
	return render_template("downloads_Organizer.html")