from flask import Blueprint, jsonify
from app.utils.jwt import token_required

users_bp = Blueprint("users", __name__, url_prefix="/users")

@users_bp.route("/", methods=["GET"])
@token_required
def list_users(user_data):
    return jsonify({"msg": "Ruta protegida de usuarios", "user": user_data}), 200
