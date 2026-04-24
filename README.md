# Flask Notes API

## Description

This is a Flask REST API that allows users to register, log in, and manage personal notes. Each user can only access their own notes. The project demonstrates authentication, authorization, and full CRUD operations.

## Features

- User registration and login
- Session-based authentication
- Password hashing using Flask-Bcrypt
- Create, read, update, and delete notes
- Protected routes (users can only access their own notes)
- Pagination for notes

## Technologies Used

- Python
- Flask
- Flask-SQLAlchemy
- Flask-Bcrypt
- Flask-Migrate
- Marshmallow

## Project Structure

- app.py: Main application entry point
- config.py: Configuration settings
- models.py: Database models (User, Note)
- schemas.py: Marshmallow schemas
- extensions.py: Database and bcrypt initialization
- routes/auth.py: Authentication routes
- routes/notes.py: Notes CRUD routes
- seed.py: Database seeding script

## Setup Instructions

git clone https://github.com/YOUR_USERNAME/YOUR_REPO.git
cd YOUR_REPO
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

Create a .env file with:
SECRET_KEY=dev-secret-key
DATABASE_URL=sqlite:///app.db

flask db init
flask db migrate -m "initial migration"
flask db upgrade

python seed.py

flask run

## API Endpoints

Authentication:
POST /auth/signup
POST /auth/login
POST /auth/logout
GET /auth/me

Notes (Protected):
GET /api/notes
POST /api/notes
GET /api/notes/<id>
PATCH /api/notes/<id>
DELETE /api/notes/<id>

## Pagination

/api/notes?page=1
Default limit is 5 notes per page

## Status Codes

200 Success
201 Created
204 No content
400 Bad request
401 Unauthorized
403 Forbidden
404 Not found