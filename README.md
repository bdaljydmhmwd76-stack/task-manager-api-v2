# Task Manager RESTful API

A lightweight RESTful API built with Python and Flask to manage daily tasks through standard CRUD (Create, Read, Update, Delete) operations.

---

## 📌 Features & Data Model

Each Task record contains the following fields:
- `id`: Unique identifier (Auto-generated integer).
- `title`: Task title (**Mandatory**, non-empty string).
- `description`: Detailed task information (Optional string).
- `status`: Current state (`pending` or `completed`, default is `pending`).
- `created_at`: ISO format UTC timestamp (Auto-generated).

---

## 🛠️ API Endpoints Summary

| Method | Endpoint | Description | HTTP Status Codes |
| :--- | :--- | :--- | :--- |
| **POST** | `/tasks` | Create a new task | `201 Created`, `400 Bad Request` |
| **GET** | `/tasks` | Retrieve all tasks | `200 OK` |
| **GET** | `/tasks/<id>` | Retrieve a specific task by ID | `200 OK`, `404 Not Found` |
| **PUT/PATCH** | `/tasks/<id>` | Update an existing task | `200 OK`, `400 Bad Request`, `404 Not Found` |
| **DELETE** | `/tasks/<id>` | Remove a task by ID | `200 OK`, `404 Not Found` |

---

## 🚀 Setup & Execution Instructions

### Prerequisites
- Python 3.x installed.

### Installation & Local Run
1. **Clone the repository:**
   ```bash
   git clone [https://github.com/bdaljydmhmwd76-stack/task-manager-api-v2.git](https://github.com/bdaljydmhmwd76-stack/task-manager-api-v2.git)
   cd task-manager-api-v2
   # task-manager-api-v2
