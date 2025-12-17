import traceback

from flask import Blueprint, jsonify

bp = Blueprint("main", __name__)

@bp.route("/api_inference/query", methods=["POST"])
def query(prompt: str):
    try:
        print("prompt", prompt)
        return jsonify( {
            "response": "Ciao Bello MIO!",
        } ), 200

    except Exception as ex:
        traceback.print_exc()
        return jsonify( {"error": str(ex)} ), 500


@bp.route("/api_inference/health", methods=["GET"])
def health():
    return jsonify({"status": "success"}), 200