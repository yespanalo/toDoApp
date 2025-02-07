from flask import Blueprint, jsonify, request
from services.priorities_service import PrioritiesService

priorities_bp = Blueprint('priorities_bp', __name__)

@priorities_bp.route('/queryPriorities', methods = ["GET"])
def getPriorities():
    response = PrioritiesService.get_all_priorities()
    return jsonify(response)