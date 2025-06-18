# IT Company Task Manager 🧑‍💻

A simple web application built with Django for managing tasks, workers, positions, and tags in an IT company.

## Features

- Authentication and authorization (admin and regular users)
- Task CRUD: create, update, delete, view tasks
- Assign workers and tags to tasks
- Position and worker management (only for admins)
- Task filtering and searching by name
- Responsive and styled UI with custom backgrounds
- Display completed and uncompleted tasks in the employee profile
- Only superusers can:

    Create, delete positions

    Create, promote workers

    Delete other users

    Access multi-delete position form

## Tech Stack

- Python 3.11
- Django 4.x
- SQLite (default)
- HTML + TailwindCSS (via CDN)
- crispy-forms (optional)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/shinodegu/it-company-task-manager
   cd task-manager

2. Create a virtual environment
    python -m venv venv
    source venv/bin/activate  # or venv\Scripts\activate on Windows

3. Install dependencies
    pip install -r requirements.txt

4. Run migrations and create superuser
    python manage.py migrate
    python manage.py createsuperuser

5. Run the development server
    python manage.py runserver
   
6. Users to test site functionality
    login: not_admin
    password: Vba>TdHN 
    login: admin
    password: admin_123
