from flask import Blueprint, jsonify, request
from services.user_service import UserService

user_bp = Blueprint('user_bp', __name__)

@user_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    response = UserService.login(email, password)
    return jsonify(response)

@user_bp.route('/QueryUsers', methods = ["GET"])
def getUsers():
    response = UserService.get_all_users()
    return jsonify(response)