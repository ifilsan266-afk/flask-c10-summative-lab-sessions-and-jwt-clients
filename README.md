# Productivity Notes API

## Description

A secure Flask REST API for a personal productivity notes application. Users can register, log in, and manage their own private notes. Each note belongs to a single user, and users cannot access each other's data. Authentication is handled via Flask sessions.

---

## Technologies Used

- Python 3.8+
- Flask 2.2.2
- Flask-SQLAlchemy 3.0.3
- Flask-Migrate 4.0.0
- Flask-Bcrypt 1.0.1
- Marshmallow 3.20.1
- Faker 15.3.2
- Pipenv

---

## Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/productivity-api.git
cd productivity-api
```

### 2. Install dependencies

```bash
pipenv install
```

### 3. Activate the virtual environment

```bash
pipenv shell
```

### 4. Set up the database

```bash
flask db init
flask db migrate -m "initial migration"
flask db upgrade
```

### 5. Seed the database

```bash
python seed.py
```

### 6. Run the application

```bash
flask run
```

The API will be available at `http://127.0.0.1:5000`

---

## API Endpoints

### Authentication

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/signup` | Register a new user | No |
| POST | `/login` | Log in a user | No |
| DELETE | `/logout` | Log out current user | Yes |
| GET | `/me` | Get current logged-in user | Yes |

### Notes

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/notes` | Get all notes (paginated) | Yes |
| POST | `/notes` | Create a new note | Yes |
| GET | `/notes/<id>` | Get a single note | Yes |
| PATCH | `/notes/<id>` | Update a note | Yes |
| DELETE | `/notes/<id>` | Delete a note | Yes |

---

## Pagination

The `GET /notes` endpoint supports pagination via query parameters:

```
GET /notes?page=1&per_page=5
```

Response includes:
```json
{
  "notes": [...],
  "total": 15,
  "pages": 3,
  "current_page": 1
}
```

---

## Example Request Bodies

### POST /signup
```json
{
  "username": "filsan",
  "password": "password123"
}
```

### POST /login
```json
{
  "username": "filsan",
  "password": "password123"
}
```

### POST /notes
```json
{
  "title": "My first note",
  "content": "This is the content of my note.",
  "category": "personal"
}
```

Valid `category` values: `general`, `work`, `personal`, `health`, `finance`

---

## Test Credentials (after seeding)

| Username | Password |
|----------|----------|
| filsan | password123 |
| trainer_jane | password123 |
| john_doe | password123 |

---

## Status Codes

| Code | Meaning |
|------|---------|
| 200 | OK |
| 201 | Created |
| 204 | No Content |
| 400 | Bad Request |
| 401 | Unauthorized |
| 403 | Forbidden |
| 404 | Not Found |
| 422 | Unprocessable Entity |
