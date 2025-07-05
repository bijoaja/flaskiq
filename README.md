# 📢 **Template Flask - Bijoaja** 💪

## 📌 **DESCRIBE**

Bijoaja is a Flask project template designed to accelerate the development of web applications based on Python Flask efficiently and structurally. This template is suitable as a foundation for various types of applications, ranging from information systems, backend APIs, to analytical dashboards.With a tidy structure and ready-to-use features, developers can immediately focus on business logic without having to think about the repetitive initial setup.

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
│   │   ├── feature/
│   │   ├   ├── __init__.py
│   │   ├   ├── models.py
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

## ⚙️ **Installation**
### 1️⃣ Clone Repository

```sh
 git clone https://github.com/bijoaja/template_flask.git your_directory
 cd your_directory
```

### 2️⃣ Create Virtual Environment & Install Dependencies
```sh
 python -m venv your_name_venv                # Flexibel your_name_venv
 source your_name_venv/bin/activate           # for Linux/Mac
 source your_name_venv/scripts/activate       # for Windows
 pip install -r requirements.txt
```

### 3️⃣ set the .env

Change the value in file **.env**:

```sh
 mv .env.example .env
```

### 4️⃣ Run Applications

```sh
 flask run
```

Application run on localhost `http://127.0.0.1:<your_port>/`
default port: 8080

## 🛠️ Tech stack

- **Server**: Flask, Flask-RESTful, Flask-JWT-Extended, Flask-SQLAlchemy
- **Database**: postgresql ORM
- **Authenthications**: JWT Token Authentication

## ⚙️ Requirements System
- **FLASK 3.1**
- **PYTHON 11.3**

## 📡 Endpoint API (Summary)

| Endpoint        | Method    | Role                       | Description            |
| --------------- | --------- | -------------------------- | ---------------------  |
| `/api/`         | GET       | ALL                        | Home API               |
| `/api/docs`     | GET       | ALL                        | Documentation API      |

## 🤝 Contribution

Developed by @bijoaja 💌.

## 📧 Contact

if you have questions or problems, please contact via email: [**BIJOAJA**](mailto\:joelbinsar@gmail.com).

---

# 📢 **Template Flask - Bijoaja** 💪