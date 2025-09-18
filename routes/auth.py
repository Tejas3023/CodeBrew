from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from models.user_models import create_user
from config.db import mongo

# Define blueprint
auth_bp = Blueprint("auth", __name__)

# -----------------------------
# Register (signup) route
# -----------------------------
@auth_bp.route("/register", methods=["POST"])
def register():
    try:
        data = request.json
        if not data or not all(k in data for k in ("username", "email", "password")):
            return jsonify({"error": "Missing fields"}), 400

        # Check if user already exists
        if mongo.db.users.find_one({"email": data["email"]}):
            return jsonify({"error": "User already exists"}), 400

        hashed_pw = generate_password_hash(data["password"])
        user = create_user(data["username"], data["email"], hashed_pw)

        return jsonify({"msg": "User created", "user": user}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# -----------------------------
# Login route
# -----------------------------
@auth_bp.route("/login", methods=["POST"])
def login():
    try:
        data = request.json
        if not data or not all(k in data for k in ("email", "password")):
            return jsonify({"error": "Missing fields"}), 400

        user = mongo.db.users.find_one({"email": data["email"]})
        if not user:
            return jsonify({"error": "Invalid email or password"}), 401

        if not check_password_hash(user["password"], data["password"]):
            return jsonify({"error": "Invalid email or password"}), 401

        return jsonify({
            "msg": "Login successful",
            "user": {
                "username": user["username"],
                "email": user["email"],
                "points": user.get("points", 0)
            }
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
