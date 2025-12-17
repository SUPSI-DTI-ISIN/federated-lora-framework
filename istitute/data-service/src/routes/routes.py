import traceback

from flask import Blueprint, jsonify

bp = Blueprint("main", __name__)

@bp.route("/api_data/upload", methods=["POST"])
def upload():
    try:
        return jsonify( {
            "response": "Ciao Bello MIO! from Data Service",
        } ), 200

    except Exception as ex:
        traceback.print_exc()
        return jsonify( {"error": str(ex)} ), 500


@bp.route("/api_data/health", methods=["GET"])
def health():
    return jsonify({"status": "success"}), 200