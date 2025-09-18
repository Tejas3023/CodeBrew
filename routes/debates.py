from flask import Blueprint, request, jsonify
from models.debate_model import create_debate, get_all_debates
from models.arguement_model import add_argument, get_arguments_for_debate
from services.llama_service import generate_counterargument, summarize_debate
from services.factcheck_service import fact_check_wikidata  # only Wikidata now

debates_bp = Blueprint("debates", __name__)

# -----------------------------
# List all debates
# -----------------------------
@debates_bp.route("/", methods=["GET"])
def list_debates():
    debates = get_all_debates()
    return jsonify(debates)

# -----------------------------
# Create a new debate
# -----------------------------
@debates_bp.route("/create", methods=["POST"])
def new_debate():
    data = request.json
    debate = create_debate(
        data["title"],
        data.get("description", ""),
        data["created_by"]
    )
    return jsonify({"msg": "Debate created", "debate": debate}), 201

# -----------------------------
# Post a new argument
# -----------------------------
@debates_bp.route("/<debate_id>/argument", methods=["POST"])
def post_argument(debate_id):
    data = request.json
    user_id = data.get("user_id")
    content = data.get("content")
    stance = data.get("stance")  # "for" or "against"

    if not user_id or not content or stance not in ["for", "against"]:
        return jsonify({"error": "Missing or invalid fields"}), 400

    # 1️⃣ Save argument to DB
    argument = add_argument(debate_id, user_id, content, stance)

    # 2️⃣ Run LLaMA counterargument
    counterargument = generate_counterargument(content, stance)

    # 3️⃣ Run Wikidata fact-check
    fact_wikidata = fact_check_wikidata(content)
    fact_check_result = {"wikidata": fact_wikidata}

    # 4️⃣ Return everything in JSON
    response = {
        "argument": argument,
        "counterargument": counterargument,
        "fact_check": fact_check_result
    }

    return jsonify(response), 201

# -----------------------------
# Get all arguments for a debate
# -----------------------------
@debates_bp.route("/<debate_id>/arguments", methods=["GET"])
def get_arguments(debate_id):
    arguments = get_arguments_for_debate(debate_id)
    return jsonify(arguments)
