from flask import Blueprint, jsonify, request
from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.models import db, User, Todo
from datetime import datetime

api_bp = Blueprint('api', __name__)

@api_bp.route('/login', methods=['POST'])
def api_login():
    data = request.get_json()
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({"message": "Username and password required"}), 400

    user = User.query.filter_by(username=data['username']).first()
    if user and check_password_hash(user.password_hash, data['password']):
        access_token = create_access_token(identity=str(user.id))
        return jsonify(access_token=access_token), 200

    return jsonify({"message": "Invalid username or password"}), 401

@api_bp.route('/tasks', methods=['GET'])
@jwt_required()
def get_tasks():
    current_user_id = int(get_jwt_identity())
    tasks = Todo.query.filter_by(user_id=current_user_id).all()
    
    result = []
    for task in tasks:
        result.append({
            'id': task.id,
            'title': task.title,
            'status': task.status,
            'priority': task.priority,
            'due_date': task.due_date.strftime('%Y-%m-%d') if task.due_date else None,
            'complete': task.complete
        })
        
    return jsonify({"tasks": result}), 200

@api_bp.route('/tasks', methods=['POST'])
@jwt_required()
def create_task():
    current_user_id = int(get_jwt_identity())
    data = request.get_json()
    
    if not data or 'title' not in data:
        return jsonify({"message": "Title is required"}), 400
        
    due_date = None
    if 'due_date' in data and data['due_date']:
        try:
            due_date = datetime.strptime(data['due_date'], '%Y-%m-%d')
        except ValueError:
            return jsonify({"message": "Invalid date format. Use YYYY-MM-DD"}), 400

    new_task = Todo(
        title=data['title'],
        priority=data.get('priority', 'Medium'),
        status='Pending',
        complete=False,
        due_date=due_date,
        user_id=current_user_id
    )
    
    db.session.add(new_task)
    db.session.commit()
    
    return jsonify({
        "message": "Task created successfully",
        "task": {
            "id": new_task.id,
            "title": new_task.title,
            "status": new_task.status,
            "priority": new_task.priority,
            "due_date": new_task.due_date.strftime('%Y-%m-%d') if new_task.due_date else None
        }
    }), 201

@api_bp.route('/tasks/<int:task_id>', methods=['PUT'])
@jwt_required()
def update_task(task_id):
    current_user_id = int(get_jwt_identity())
    task = Todo.query.get(task_id)
    
    if not task:
        return jsonify({"message": "Task not found"}), 404
        
    if task.user_id != current_user_id:
        return jsonify({"message": "Unauthorized"}), 403
        
    data = request.get_json()
    if not data:
        return jsonify({"message": "No data provided"}), 400
        
    if 'title' in data:
        task.title = data['title']
    if 'status' in data:
        task.status = data['status']
        task.complete = (task.status == 'Completed')
    if 'priority' in data:
        task.priority = data['priority']
        
    if 'due_date' in data:
        if data['due_date']:
            try:
                task.due_date = datetime.strptime(data['due_date'], '%Y-%m-%d')
            except ValueError:
                return jsonify({"message": "Invalid date format. Use YYYY-MM-DD"}), 400
        else:
            task.due_date = None
            
    db.session.commit()
    
    return jsonify({
        "message": "Task updated successfully",
        "task": {
            "id": task.id,
            "title": task.title,
            "status": task.status,
            "priority": task.priority,
            "due_date": task.due_date.strftime('%Y-%m-%d') if task.due_date else None,
            "complete": task.complete
        }
    }), 200

@api_bp.route('/tasks/<int:task_id>', methods=['DELETE'])
@jwt_required()
def delete_task(task_id):
    current_user_id = int(get_jwt_identity())
    task = Todo.query.get(task_id)
    
    if not task:
        return jsonify({"message": "Task not found"}), 404
        
    if task.user_id != current_user_id:
        return jsonify({"message": "Unauthorized"}), 403
        
    db.session.delete(task)
    db.session.commit()
    
    return jsonify({"message": "Task deleted successfully"}), 200
