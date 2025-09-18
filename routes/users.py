from flask import Blueprint, jsonify
from config.db import mongo

users_bp = Blueprint("users", __name__)

@users_bp.route("/leaderboard", methods=["GET"])
def leaderboard():
    users = list(mongo.db.users.find().sort("points", -1).limit(10))
    return jsonify(users)
