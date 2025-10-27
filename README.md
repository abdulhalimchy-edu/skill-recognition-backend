# Skill Recogintion Backend

A web application built with [Django](https://www.djangoproject.com/), a high-level Python web framework that encourages rapid development and clean, pragmatic design.

---

### Create and activate virtual environment
```
python -m venv venv
# On macOS/Linux
source venv/bin/activate
# On Windows
venv\Scripts\activate
```

### Install Dependencies
```
pip install -r requirements.txt
```

### Create PostgreSQL Database
Install postgres in your local machine or you can use remote postres database provided by cloud server

### Create .env file and set environment variables
```
ENV_TYPE="DEVELOPMENT"
SECRET_KEY="dja-7jx4nf36$3"

DB_NAME="db_skill"
DB_USER="admin"
DB_PASSWORD="admin"
DB_HOST="localhost"
DB_PORT="5432"

RUNPOD_API_ENDPOINT=""
RUNPOD_API_ACCESS_KEY=""

RAPID_API_KEY=""
```

### Apply database migrations
```
python manage.py migrate
```

### Run the project
```
python manage.py runserver
```
