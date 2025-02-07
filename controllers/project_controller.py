from flask import Blueprint, jsonify, request
from services.projects_service import ProjectsService

projects_bp = Blueprint('projects_bp', __name__)

@projects_bp.route('/QueryProjects', methods=["GET"])
def get_projects():
    project_id = request.args.get("id")  # Get the 'id' parameter from the request

    if project_id:
        response = ProjectsService.get_project_by_id(project_id)
    else:
        response = ProjectsService.get_all_projects()

    return jsonify(response)

@projects_bp.route('/MutationCreateProjects', methods=['POST'])
def create_project():
    data = request.get_json()
    name = data.get('name')
    description = data.get('description')
    created_by = data.get('created_by')
    response = ProjectsService.create_project(name, description, created_by)
    return jsonify(response)