from flask import Flask
from config import Config # For Database Configuration Settings
from models import db # For Database Object
# Blueprints for accessing the API Routes
from view_api import view_bp
from app_api import api_bp

def create_app():
    app = Flask(__name__) # Main Backend Instance
    
    # 1. Load the config from the class "Config" (DB config)
    app.config.from_object(Config)

    # 2. Connect the database object to the app
    db.init_app(app)

    # Registering both "groups"
    app.register_blueprint(view_bp) # Home page, Dashboard page
    app.register_blueprint(api_bp, url_prefix='/api') # /api/start, /api/status


    with app.app_context():
        db.create_all() # Creates tasks.db based on Config settings

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)


