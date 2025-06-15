# 📢 **Template Flask - Bijoaja** 💪

## 📌 **DESCRIBE**

Ganesha AI is a tool to help tenant members in running sports. Ganesha AI can be considered an AI-based Assistant that is able to respond to members appropriately, quickly and usefully. Ganesha AI is built on OpenAI and MediaPipe as a base model.

## **Structur Project**
```
template_flask/
├── app/
│   ├── __init__.py
│   ├── routes.py
│   ├── controller/
│   │   ├── *Controller.py
│   ├── service/
│   │   ├── *_service.py
│   ├── model/
│   │   ├── __init__.py
│   │   ├── models.py
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
 git clone https://github.com/bijoaja/template_flask.git
 cd template_flask
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