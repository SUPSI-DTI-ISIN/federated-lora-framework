import traceback

from flask import Blueprint, jsonify

from services.model import ModelService

bp = Blueprint("main", __name__)

@bp.route("/api_inference/query", methods=["POST"])
def query(prompt: str):
    try:
        response = ModelService.inference_model(prompt=prompt)
        return jsonify( {
            "response": response,
        } ), 200

    except Exception as ex:
        traceback.print_exc()
        return jsonify( {"error": str(ex)} ), 500


@bp.route("/api_inference/health", methods=["GET"])
def health():
    return jsonify({"status": "success"}), 200