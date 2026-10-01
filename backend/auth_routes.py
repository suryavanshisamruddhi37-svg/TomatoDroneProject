from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import os
import json
import secrets

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")

USERS_FILE = os.path.join(os.path.dirname(__file__), "users.json")


def load_users():
    if not os.path.exists(USERS_FILE):
        return []

    try:
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    except:
        return []


def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=4)


@auth_bp.route("/register", methods=["POST"])
def register():

    data = request.get_json()

    if not data:
        return jsonify({
            "message": "Invalid request"
        }), 400

    name = data.get("name", "").strip()
    email = data.get("email", "").strip().lower()
    password = data.get("password", "")

    if not name or not email or not password:
        return jsonify({
            "message": "Name, email and password are required"
        }), 400

    users = load_users()

    for user in users:
        if user["email"] == email:
            return jsonify({
                "message": "Email already registered"
            }), 409

    user = {
        "id": len(users) + 1,
        "name": name,
        "email": email,
        "password": generate_password_hash(password)
    }

    users.append(user)
    save_users(users)

    token = secrets.token_hex(32)

    response_user = {
        "id": user["id"],
        "name": user["name"],
        "email": user["email"]
    }

    return jsonify({
        "token": token,
        "user": response_user,
        "message": "Registration successful"
    }), 201


@auth_bp.route("/login", methods=["POST"])
def login():

    data = request.get_json()

    if not data:
        return jsonify({
            "message": "Invalid request"
        }), 400

    email = data.get("email", "").strip().lower()
    password = data.get("password", "")

    if not email or not password:
        return jsonify({
            "message": "Email and password are required"
        }), 400

    users = load_users()

    for user in users:

        if user["email"] == email:

            if check_password_hash(user["password"], password):

                token = secrets.token_hex(32)

                response_user = {
                    "id": user["id"],
                    "name": user["name"],
                    "email": user["email"]
                }

                return jsonify({
                    "token": token,
                    "user": response_user,
                    "message": "Login successful"
                })

            return jsonify({
                "message": "Invalid email or password"
            }), 401

    return jsonify({
        "message": "Invalid email or password"
    }), 401