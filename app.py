from flask import Flask, jsonify, request
from datetime import datetime

app = Flask(__name__)

# In-memory storage for tasks
tasks = []
task_id_counter = 1

# Helper function to find a task by ID
def find_task(task_id):
    return next((task for task in tasks if task["id"] == task_id), None)

# 1. POST /tasks - Create a new task
@app.route('/tasks', methods=['POST'])
def create_task():
    global task_id_counter
    data = request.get_json()

    # Validation: title is required and cannot be empty
    if not data or 'title' not in data or not str(data['title']).strip():
        return jsonify({"error": "Title is mandatory and cannot be empty"}), 400

    new_task = {
        "id": task_id_counter,
        "title": str(data['title']).strip(),
        "description": data.get('description', ''),
        "status": data.get('status', 'pending'),
        "created_at": datetime.utcnow().isoformat() + "Z"
    }

    tasks.append(new_task)
    task_id_counter += 1
    return jsonify(new_task), 201

# 2. GET /tasks - Retrieve all tasks
@app.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify(tasks), 200

# 3. GET /tasks/{id} - Retrieve a specific task by ID
@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = find_task(task_id)
    if not task:
        return jsonify({"error": "Task not found"}), 404
    return jsonify(task), 200

# 4. PUT / PATCH /tasks/{id} - Update an existing task
@app.route('/tasks/<int:task_id>', methods=['PUT', 'PATCH'])
def update_task(task_id):
    task = find_task(task_id)
    if not task:
        return jsonify({"error": "Task not found"}), 404

    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid payload"}), 400

    # Validation: title cannot be empty if provided
    if 'title' in data:
        if not str(data['title']).strip():
            return jsonify({"error": "Title cannot be empty"}), 400
        task['title'] = str(data['title']).strip()

    if 'description' in data:
        task['description'] = data['description']

    if 'status' in data:
        task['status'] = data['status']

    return jsonify(task), 200

# 5. DELETE /tasks/{id} - Remove a task
@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = find_task(task_id)
    if not task:
        return jsonify({"error": "Task not found"}), 404

    tasks.remove(task)
    return jsonify({"message": f"Task {task_id} successfully deleted"}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)
          
