# Django Photo Album Management System

A production-ready Django application for managing photo albums using class-based views, role-based access control, Cloudinary media storage, and PostgreSQL support.

## Features
- Album and photo CRUD with Django class-based views
- Role-based access control using Django authentication and admin group permissions
- Cloudinary integration for storing all uploaded images
- PostgreSQL support through environment-configured `DATABASE_URL`
- Render-friendly configuration for production deployment

## Local Setup
1. Create a Python virtual environment and activate it.
2. Install dependencies: `pip install -r requirements.txt`
3. Copy `.env.example` to `.env` and set values for `SECRET_KEY`, `DATABASE_URL`, `CLOUDINARY_URL`, `DJANGO_DEBUG`, and `ALLOWED_HOSTS`.
4. Run migrations: `python manage.py migrate`
5. Create a superuser: `python manage.py createsuperuser`
6. Start the server: `python manage.py runserver`

## Deployment Notes
- Use `gunicorn` as the production WSGI server.
- Configure `DATABASE_URL` and `CLOUDINARY_URL` using Render environment variables.
- Set `DJANGO_DEBUG=False` in production.
- Ensure `DEFAULT_FILE_STORAGE` is set to `cloudinary_storage.storage.MediaCloudinaryStorage` when `DEBUG=False`.

## Recommended Groups
- `Album Admin`: users in this group can manage any album and photo.
- authenticated users can create and manage their own albums.

## Files
- `photoalbum/`: core Django project settings and WSGI configuration
- `albums/`: album and photo models, views, and URL routes
- `templates/`: UI templates for albums and user authentication

