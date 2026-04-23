# Notification Service

This is a Django-based notification service built as part of my microservice backend project.

The main purpose of this service is to handle notifications and real-time communication using WebSockets.

---

## What this service does

* Sends notifications
* Handles real-time communication using Django Channels
* Works as a separate service in a microservice architecture

---

## Tech Used

* Python
* Django
* Django Channels
* WebSockets
* Docker

---

## Project Structure

```text
NotificationService/
│
├── myapp/                 # App logic (consumers, models, views)
├── notificationservice/   # Main Django project
├── jwt_keys/              # JWT keys (ignored in git)
├── manage.py
├── requirements.txt
├── Dockerfile
├── .gitignore
└── README.md
```

---

## How to Run

### 1. Clone the repo

```bash
git clone https://github.com/YOUR-USERNAME/NotificationService.git
cd NotificationService
```

### 2. Create virtual environment

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run migrations

```bash
python manage.py migrate
```

### 5. Start server

```bash
python manage.py runserver
```

---

## Run with Docker

```bash
docker build -t notification-service .
docker run -p 8000:8000 notification-service
```

---

## Notes

* `.env`, `jwt_keys/`, and `.pem` files are ignored for security
* This service is part of a larger backend system

---

## Author

Azeem P H
