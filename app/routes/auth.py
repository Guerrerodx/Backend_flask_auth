from flask import Blueprint, request, jsonify
from app.utils.jwt import generate_token, verify_token
from app.utils.config import load_users, save_users, token_blacklist
from app.utils.jwt import token_required, admin_required

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    role = data.get("role", "user")

    if not username or not password:
        return jsonify({"msg": "Faltan campos requeridos"}), 400

    users = load_users()

    if any(u["username"] == username for u in users):
        return jsonify({"msg": "El usuario ya existe"}), 400

    if role == "admin":
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({"msg": "Token requerido para crear un administrador"}), 401

        if token in token_blacklist:
            return jsonify({"msg": "Token inválido (sesión cerrada)"}), 401

        user_data = verify_token(token)
        if not user_data or user_data["role"] != "admin":
            return jsonify({"msg": "Permisos insuficientes para crear un administrador"}), 403

    users = load_users()

    new_id = max((u["id"] for u in users), default=0) + 1

    new_user = {
        "id": new_id,
        "username": username,
        "password": password,
        "role": role
    }


    users.append(new_user)
    save_users(users)

    return jsonify({
        "msg": "Usuario registrado exitosamente",
        "user": {
            "id": new_user["id"],
            "username": new_user["username"],
            "role": new_user["role"]
        }
    }), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    
    users = load_users()
    user = next((u for u in users if u["username"] == username and u["password"] == password), None)
    if not user:
        return jsonify({"msg": "Credenciales inválidas"}), 401

    token = generate_token(user["id"], user["username"], user["role"])
    return jsonify({"msg": "Inicio de sesión exitoso", "token": token}), 200

@auth_bp.route('/logout', methods=['POST'])
def logout():
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({"msg": "Token requerido"}), 400

    token_blacklist.append(token)
    return jsonify({"msg": "Sesión cerrada exitosamente"}), 200

@auth_bp.route('/profile', methods=['GET'])
@token_required
def profile(current_user):
    return jsonify({
        "msg": "Acceso concedido",
        "user": {
            "id": current_user["id"],
            "username": current_user["username"],
            "role": current_user["role"]
        }
    }), 200


@auth_bp.route('/admin/dashboard', methods=['GET'])
@admin_required
def admin_dashboard(current_user):
    return jsonify({"msg": "Bienvenido al panel de administración", "admin": current_user}), 200

@auth_bp.route('/delete/<int:user_id>', methods=['DELETE'])
@admin_required
def delete_user(current_user, user_id):
    users = load_users()
    user_to_delete = next((u for u in users if u["id"] == user_id), None)

    if not user_to_delete:
        return jsonify({"msg": "Usuario no encontrado"}), 404
    if user_to_delete["username"] == current_user["username"]:
        return jsonify({"msg": "No puedes eliminarte a ti mismo"}), 400

    updated_users = [u for u in users if u["id"] != user_id]
    save_users(updated_users)
    return jsonify({"msg": f"Usuario con ID {user_id} eliminado exitosamente"}), 200

@auth_bp.route('/users', methods=['GET'])
@admin_required
def list_users(current_user):
    users = load_users()
    users_sanitized = [{"id": u["id"], "username": u["username"], "role": u["role"]} for u in users]
    return jsonify({"usuarios": users_sanitized}), 200

@auth_bp.route('/change-password', methods=['POST'])
@token_required
def change_password(current_user):
    data = request.get_json()
    current_password = data.get("current_password")
    new_password = data.get("new_password")

    if not current_password or not new_password:
        return jsonify({"msg": "Se requieren la contraseña actual y la nueva"}), 400

    users = load_users()
    for user in users:
        if user["id"] == current_user["id"]:
            if user["password"] != current_password:
                return jsonify({"msg": "La contraseña actual es incorrecta"}), 401
            user["password"] = new_password
            save_users(users)
            return jsonify({"msg": "Contraseña actualizada exitosamente"}), 200

    return jsonify({"msg": "Usuario no encontrado"}), 404
