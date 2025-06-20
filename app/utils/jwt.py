import jwt
import datetime
from functools import wraps
from flask import request, jsonify

SECRET_KEY = "mi_clave_secreta"

def generate_token(user_id, username, role):
    payload = {
        "id": user_id,
        "username": username,
        "role": role,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token

def verify_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return {
            "id": payload["id"],
            "username": payload["username"],
            "role": payload["role"]
        }
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        return None

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        from app.utils.config import token_blacklist  # ← Import aquí dentro
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({"msg": "Token requerido"}), 401

        if token in token_blacklist:
            return jsonify({"msg": "Token inválido (sesión cerrada)"}), 401

        user_data = verify_token(token)
        if not user_data:
            return jsonify({"msg": "Token inválido o expirado"}), 401

        return f(user_data, *args, **kwargs)
    return decorated

def admin_required(f):
    @wraps(f)
    @token_required
    def decorated(user_data, *args, **kwargs):
        if user_data["role"] != "admin":
            return jsonify({"msg": "Acceso restringido a administradores"}), 403
        return f(user_data, *args, **kwargs)
    return decorated
