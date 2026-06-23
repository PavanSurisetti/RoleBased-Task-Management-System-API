
# 🗂️ RoleBased Task Management System API

### A scalable and secure role-based task management system built using FastAPI, SQLAlchemy, and PostgreSQL with JWT authentication, team collaboration, and advanced task tracking features.

---

## 🚀 Live Demo

🔗 **Live API:**
[RoleBased Task Management System API](https://rolebased-task-management-system-api.onrender.com)

📄 **API Docs (Swagger UI):**
[API Documentation](https://rolebased-task-management-system-api.onrender.com/docs)

> ⚠️ Hosted on Render free tier — first request may take a few seconds due to cold starts.

---

## 🛠 Tech Stack

* **Backend Framework:** FastAPI
* **Database:** PostgreSQL (Neon)
* **ORM:** SQLAlchemy
* **Authentication:** JWT (python-jose)
* **Password Hashing:** Passlib (bcrypt)
* **Server:** Uvicorn
* **Validation:** Pydantic
* **Deployment:** Render

---

## 💡 Features

* 👤 User registration & login system
* 🔐 JWT-based authentication
* 🔑 Secure password hashing (bcrypt)
* 👥 Role-based access control (Admin & Member)
* 🏢 Team creation & management
* ➕ Add users to teams
* 📌 Task creation & assignment
* 📊 Task status tracking (TODO / IN_PROGRESS / DONE)
* 🔥 Priority management (LOW / MEDIUM / HIGH)
* 📝 Comment system on tasks
* 🔍 Filter tasks by status
* 📂 Team-wise and user-wise task views
* ⚡ Fully RESTful API design
* 📄 Interactive Swagger documentation

---

## 📂 Project Structure

```
RoleBased-Task-Management-System-API/
├── main.py              # API endpoints & business logic
├── models.py            # Database models (User, Team, Task, Comment)
├── database.py          # DB connection & session setup
├── requirements.txt     # Dependencies
├── .env                 # Environment variables
├── screenshots/         # API documentation screenshots
├── .gitignore           # Ignored files
└── README.md            # Project documentation
```

---

## ⚙️ Database Models

### 👤 User

* id
* name
* email (unique)
* password
* role (admin / member)

### 🏢 Team

* id
* name
* created_by

### 👥 TeamMember

* id
* user_id (FK)
* team_id (FK)

### 📌 Task

* id
* title
* description
* status (TODO / IN_PROGRESS / DONE)
* priority (LOW / MEDIUM / HIGH)
* assigned_to
* team_id
* created_at

### 📝 Comment

* id
* task_id (FK)
* user_id (FK)
* comment_text
* created_at

---

## 🚀 Installation & Local Setup

### 1️⃣ Clone the repository

```bash
git clone https://github.com/PavanSurisetti/RoleBased-Task-Management-System-API
```

### 2️⃣ Navigate to project

```bash
cd RoleBased-Task-Management-System-API
```

### 3️⃣ Create virtual environment

```bash
python -m venv venv
```

### 4️⃣ Activate environment

**Windows**

```bash
venv\Scripts\activate
```

**Mac/Linux**

```bash
source venv/bin/activate
```

### 5️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 6️⃣ Configure environment variables

Create a `.env` file:

```env
DATABASE_URL=your_postgresql_connection_string
SECRET_KEY=your_secret_key
ALGORITHM=HS256
```

---

### 7️⃣ Run the server

```bash
uvicorn main:app --reload
```

---

### 8️⃣ Open API docs

```
http://127.0.0.1:8000/docs
```

---

## 🔗 API Endpoints

| Method | Endpoint                  | Description              |
| ------ | ------------------------- | ------------------------ |
| GET    | `/`                       | Welcome message          |
| POST   | `/register`               | Register user            |
| POST   | `/login`                  | Login user (JWT token)   |
| GET    | `/profile`                | Get user profile         |
| POST   | `/teams`                  | Create team              |
| POST   | `/team/addTeamMembers`    | Add user to team         |
| GET    | `/team/users`             | Get team members         |
| POST   | `/task`                   | Create task (Admin only) |
| PATCH  | `/task/assign`            | Assign task              |
| PUT    | `/task/statusupdate/{id}` | Update task status       |
| DELETE | `/task/delete/{id}`       | Delete task              |
| GET    | `/admin/tasks`            | Get all tasks (Admin)    |
| GET    | `/task/mytasks`           | Get my tasks             |
| GET    | `/team/task/{id}`         | Get team tasks           |
| GET    | `/filter/{status}`        | Filter tasks by status   |
| POST   | `/add/comment`            | Add comment              |
| GET    | `/comment/task/{id}`      | Get task comments        |

---

## 🧠 How It Works

1. User registers and logs in
2. JWT token is generated for authentication
3. Admin creates teams and tasks
4. Tasks are assigned to team members
5. Users update task status
6. Comments enable collaboration
7. Admin monitors team progress

---

## 🚀 Deployment

* Hosted on **Render**
* Database: **Neon PostgreSQL**
* Environment variables securely managed
* Auto deployment via GitHub integration

---

## 🔮 Future Improvements

* Real-time updates (WebSockets)
* Email notifications for task updates
* Docker containerization
* Advanced analytics dashboard
* File attachments in tasks
* Frontend UI (React / Next.js)

---

## 📫 Contact

* GitHub: [PavanSurisetti](https://github.com/PavanSurisetti)
* LinkedIn: [Pavan Surisetti](https://www.linkedin.com/in/pavan-surisetti-b3281228b/)

---

## 📄 License

This project is licensed under the **MIT License**.
