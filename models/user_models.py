from config.db import mongo

def create_user(username, email, password_hash):
    user = {
        "username": username,
        "email": email,
        "password": password_hash,
        "points": 0
    }
    mongo.db.users.insert_one(user)
    return user
