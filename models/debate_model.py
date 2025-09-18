from config.db import mongo

def create_debate(title, description, created_by):
    debate = {
        "title": title,
        "description": description,
        "created_by": created_by,
        "arguments": []
    }
    mongo.db.debates.insert_one(debate)
    return debate

def get_all_debates():
    return list(mongo.db.debates.find())
