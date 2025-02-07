from flask import Blueprint, jsonify, request
from services.task_service import TaskService

tasks_bp = Blueprint ('tasks_bp', __name__)

@tasks_bp.route('/QueryTasks', methods = ["GET"])
def get_tasks():
    project_id = request.args.get("id")
    status_id = request.args.get("status_id")

    response = TaskService.get_task_by_id(project_id,status_id)

    return jsonify(response)

@tasks_bp.route('/QueryTaskByTaskId', methods = ["GET"])
def get_tasks_by_task_id():
    task_id = request.args.get("task_id")

    # if project_id:
    response = TaskService.get_task_by_task_id(task_id)
    # else:
    #     response = TaskService.get_all_tasks()

    return jsonify(response)

@tasks_bp.route('/MutationCreateTask', methods = ['POST'])
def create_task():
    data = request.get_json()
    title = data.get('title')
    description = data.get('description')
    project_id = data.get('project_id')
    assigned_to = data.get('assigned_to')
    priority_id = data.get('priority_id')
    created_by = data.get('created_by')
    response = TaskService.create_task(title,description,project_id,assigned_to,priority_id,created_by)
    return jsonify(response)

@tasks_bp.route('/MutationUpdateTask', methods = ["POST"])
def update_task():
    data = request.get_json()
    task_id = data.get('task_id')
    title = data.get('title')
    description = data.get('description')
    assigned_to = data.get('assigned_to')
    priority_id = data.get('priority_id')
    response = TaskService.update_task(task_id,title,description,assigned_to,priority_id)
    return jsonify(response)
    