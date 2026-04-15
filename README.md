# Flask Notes API

This is a simple Flask project that lets users register, log in, and manage notes.  
Each user can only see and manage their own notes.

---

## What this project does

- Users can create accounts (sign up)
- Users can log in and log out
- Users can create notes
- Users can view their notes
- Users can update notes
- Users can delete notes
- All notes are protected (only logged-in users can access them)
- Data is stored in a database using SQLAlchemy

---

## Technologies used

- Python
- Flask
- SQLAlchemy (database)
- Flask-Bcrypt (password hashing)
- Flask-Migrate (database migrations)
- Marshmallow (data formatting/serialization)

---

## Project Structure

- app.py → Main file that runs the app
- config.py → App settings (database, secret key)
- models.py → Database tables (User and Note)
- schemas.py → Formats data for responses
- extensions.py → Sets up database and password tools
- routes/auth.py → Login and signup routes
- routes/notes.py → CRUD routes for notes
- seed.py → Adds sample data to the database

---

## How to run the project

### 1. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate