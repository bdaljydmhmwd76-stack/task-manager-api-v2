from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# Configure SQLite Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Task Model Definition
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(20), default='pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "status": self.status,
            "created_at": self.created_at.isoformat() + "Z"
        }

# Initialize Database Tables
with app.app_context():
    db.create_all()

# 1. POST /tasks - Create a new task
@app.route('/tasks', methods=['POST'])
def create_task():
    data = request.get_json()

    if not data or 'title' not in data or not str(data['title']).strip():
        return jsonify({"error": "Title is mandatory and cannot be empty"}), 400

    new_task = Task(
        title=str(data['title']).strip(),
        description=data.get('description', ''),
        status=data.get('status', 'pending')
    )

    db.session.add(new_task)
    db.session.commit()

    return jsonify(new_task.to_dict()), 201

# 2. GET /tasks - Retrieve all tasks
@app.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = Task.query.all()
    return jsonify([task.to_dict() for task in tasks]), 200

# 3. GET /tasks/{id} - Retrieve a specific task by ID
@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = Task.query.get(task_id)
    if not task:
        return jsonify({"error": "Task not found"}), 404
    return jsonify(task.to_dict()), 200

# 4. PUT / PATCH /tasks/{id} - Update an existing task
@app.route('/tasks/<int:task_id>', methods=['PUT', 'PATCH'])
def update_task(task_id):
    task = Task.query.get(task_id)
    if not task:
        return jsonify({"error": "Task not found"}), 404

    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid payload"}), 400

    if 'title' in data:
        if not str(data['title']).strip():
            return jsonify({"error": "Title cannot be empty"}), 400
        task.title = str(data['title']).strip()

    if 'description' in data:
        task.description = data['description']

    if 'status' in data:
        task.status = data['status']

    db.session.commit()
    return jsonify(task.to_dict()), 200

# 5. DELETE /tasks/{id} - Remove a task
@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = Task.query.get(task_id)
    if not task:
        return jsonify({"error": "Task not found"}), 404

    db.session.delete(task)
    db.session.commit()
    return jsonify({"message": f"Task {task_id} successfully deleted"}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)
        
