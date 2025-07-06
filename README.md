# 📢 **Template Flask - Bijoaja** 💪

## 📌 **DESCRIBE**

<b>Bijoaja is a Flask project template designed to accelerate the development of web applications based on Python Flask efficiently and structurally. This template is suitable as a foundation for various types of applications, ranging from information systems, backend APIs, to analytical dashboards.With a tidy structure and ready-to-use features, developers can immediately focus on business logic without having to think about the repetitive initial setup.</b>

## **⚙️ Main Feature**
- 🔁 Modular and Scalable Folder Structure
- 🔐 Authentication & Authorization (Optional)
- 🌐 Dynamic Routing and Blueprints
- 📦 ORM Integration (SQLAlchemy / others)
- 📊 Support for API & HTML Templates (Jinja2)
- 🧪 Ready for Testing (Unit Test / Pytest)
- 🔧 Support for .env, Config Class, and Error Handling
- 🚀 Ready for Deployment (Gunicorn, Docker, etc.)
- 🤖 Support for AI Integration (openai, grok, local model, etc)

## **👨‍💻 Support for**
- Beginner to intermediate Flask developers
- Students for web-based final projects
- Researchers or Data Scientists who want to quickly create dashboards or APIs

## **📁 Project Structur**
```
template_flask/
├── app/
│   ├── __init__.py
│   ├── routes.py
│   ├── controller/
│   │   ├── feature/
│   │   ├   ├──*Controller.py
│   ├── service/
│   │   ├── feature
│   │   ├   ├── *_service.py
│   ├── model/
│   │   ├── __init__.py
│   │   ├── *model.py
├── utils/
│   ├── __init__.py
│   ├── *.py
├── config.py
├── server.py
├── requirements.txt
├── .gitignore
├── .env.example
└── README.md
```

## ⚙️ **Installation and Usage**
### 1️⃣ Clone Repository

```sh
 git clone https://github.com/bijoaja/template_flask.git your_directory
 cd your_directory
```

### 2️⃣ Run with Virtual Environment (VENV)

#### <h3> <li> ✅ Create Virtual Environment & Install Dependencies
```sh
 python -m venv your_name_venv                # Flexibel your_name_venv
 source your_name_venv/bin/activate           # for Linux/Mac
 source your_name_venv/scripts/activate       # for Windows
 pip install -r requirements.txt
```

#### <h3> <li> ⚙️ Setup Environment Variables

Change the value in file **.env**:

```sh
 mv .env.example .env
```

#### <h3> <li> 🚀 Run Applications

```sh
 flask run
```

### 3️⃣ Run with Docker

#### <h3> <li> 🐳 Install Docker Desktop
<b> Download and install Docker Desktop:
👉 [**Install Docker**](href:https://docs.docker.com/desktop/)

#### <h3> <li> 🔧 Build and Start Container

```sh
 docker-compose up --build -d
```

#### <h3> <li> ♻️ Restart Docker (if have change code)

```sh
 docker-compose restart template_flask_web
```

<b> Application run on localhost `http://127.0.0.1:<your_port>/`
default port: 8080

## 🛠️ Tech stack

- **Server**: Flask, Flask-RESTful, Flask-JWT-Extended, Flask-SQLAlchemy
- **Database**: postgresql ORM
- **Authenthications**: JWT Token Authentication

## ⚙️ Requirements System
- **FLASK 3.1**
- **PYTHON3 12**

## 📡 Endpoint API (Summary)

| Endpoint        | Method    | Role                       | Description            |
| --------------- | --------- | -------------------------- | ---------------------  |
| `/    `         | GET       | ALL                        | Home view              |
| `/api/`         | GET       | ALL                        | Home API               |
| `/api/docs`     | GET       | ALL                        | Documentation API      |

## 🤝 Contribution

Developed by @bijoaja 💌.

## 📧 Contact

if you have questions or problems, please contact via email: [**BIJOAJA**](mailto\:joelbinsar@gmail.com).

---

# 📢 **Template Flask - Bijoaja** 💪