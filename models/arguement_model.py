from config.db import mongo
from datetime import datetime
from bson import ObjectId

def add_argument(debate_id, user_id, text, stance):
    """
    Save an argument under a debate in the 'debates' collection.
    """
    # Convert debate_id to ObjectId for MongoDB query
    debate_obj_id = ObjectId(debate_id)

    # Create argument with unique ObjectId
    argument = {
        "_id": ObjectId(),
        "user_id": user_id,
        "text": text,
        "stance": stance,  # "for" or "against"
        "votes": 0,
        "created_at": datetime.utcnow()
    }

    # Push argument into debate
    mongo.db.debates.update_one(
        {"_id": debate_obj_id},
        {"$push": {"arguments": argument}}
    )

    # Convert ObjectId to string before returning
    argument["_id"] = str(argument["_id"])
    return argument

def get_arguments_for_debate(debate_id):
    """
    Fetch all arguments for a debate in JSON-friendly format.
    """
    debate_obj_id = ObjectId(debate_id)
    debate = mongo.db.debates.find_one({"_id": debate_obj_id})
    if not debate:
        return []

    arguments = debate.get("arguments", [])

    # Convert all ObjectIds to strings
    for arg in arguments:
        if isinstance(arg["_id"], ObjectId):
            arg["_id"] = str(arg["_id"])

    return arguments
