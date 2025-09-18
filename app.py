import sys
import os

# Ensure project root is in Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from flask import Flask
from flask_cors import CORS
from config.db import init_db

# Import blueprints
from routes.auth import auth_bp
from routes.debates import debates_bp
from routes.users import users_bp

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # allow frontend requests

# Connect to MongoDB
init_db(app)

# Register blueprints
app.register_blueprint(auth_bp, url_prefix="/api/auth")
app.register_blueprint(debates_bp, url_prefix="/api/debates")
app.register_blueprint(users_bp, url_prefix="/api/users")

# Run the app
if __name__ == "__main__":
    app.run(debug=True, port=5000)
