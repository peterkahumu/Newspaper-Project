# Newspaper Project

A simple Django-based news website (local development project) with three main apps:
- `accounts` — custom user model and registration/auth flows
- `articles` — article CRUD (create, list, detail, edit, delete)
- `pages` — static pages (home, about, etc.)

This repository contains the Django project `newspaper_project` and templates under `templates/` for rendering pages and authentication.


## Features

- Custom user model (in `accounts`) with registration and authentication views and templates
- Password reset, and password change features.
- Article creation, editing, deletion and listing (in `articles`)
- Basic static pages served from `pages`
- Ready-to-use templates and navigation component

## Prerequisites

- Python 3.12.3+ (project was developed with Python 3.12.3+)
- pip
- (Optional) virtualenv or venv

## Quickstart (development)

1. Clone the repository (if you haven't already):

   ```python
   git clone https://github.com/peterkahumu/Newspaper-Project.git
   cd newspaper_project
   ```

2. Create and activate a virtual environment (recommended):

   ```python
   python3 -m venv .venv

   # linux and macos
   source .venv/bin/activate

   #windows
   source .venv/Scripts/activate
   ```

3. Install dependencies:

   ```python
   pip install -r requirements.txt
   ```

4. Database and migrations (uses `POSTGRES`):

   ```python
   python manage.py migrate
   ```

5. Create a superuser to access the admin:

   ```python
   python manage.py createsuperuser
   ```

6. Run the development server:

   ```python
   python manage.py runserver
   ```

Open http://127.0.0.1:8000 in your browser.

## Environment & configuration

1. Please create a `.env` file in the root project folder.
2. Run the following command in your terminal.
```bash
cp .env_example .env
```
3. Create a postgres database and enter the credentials in the appropriate tags.
4. Provide a secret key next to the `SECRET_KEY` variable.

> NB: Please make sure that `.env` is added to `.gitignore` to avoid uploading sensitive information to the cloud.
## Running tests

Run the project's tests with Django's test runner:

   ```python
   python manage.py test
   ```

This will run tests in the `accounts`, `articles`, and `pages` apps (if present).

## Admin

Access the Django admin at `http:8000/admin/` after creating a superuser. The admin includes models registered by the apps (such as Article and the custom User model).

## Templates & Static

- Templates are in `templates/` and the apps use template names under `templates/articles/`, `templates/registration/`, and `templates/components/`.
- Static assets are expected in `static/`.

## Development notes & suggestions

- The repository already uses a custom user model (see `accounts/models.py`). When switching databases or testing migrations, ensure you migrate `accounts` first.
- If you add third-party packages, pin them into `requirements.txt` and include notes in this README..
- Consider adding `black`, `flake8`/`ruff`, and pre-commit hooks for code quality.

## Contributing

1. Fork the repository and create a feature branch:

   ```python
   git checkout -b feat/my-feature
   ```

2. Make changes and run tests locally.
3. Open a pull request describing your changes.

Keep changes small and focused. Add tests for new functionality when possible.

## Deployment

This README includes only minimal production guidance. Typical steps:

- Configure a production database (Postgres recommended)
- Add a WSGI/ASGI server (Gunicorn/uvicorn) behind a reverse proxy (NGINX)
- Set `DEBUG = False`, update `ALLOWED_HOSTS`, and set a secure `SECRET_KEY`
- Serve static files via CDN or NGINX after running `python manage.py collectstatic`

## Troubleshooting

- "Migrations conflict" or missing tables: run `python manage.py makemigrations`/`migrate`. If you changed the custom user model after initial migrations, restoring a clean DB may be required.
- Template not found: check `TEMPLATES` DIRS in `newspaper_project/settings.py` and ensure `templates/` is included.

## License

This project includes a `LICENSE` file in the repository root. Check that file for license details.

## Contact

If you need help maintaining or extending this project, open an issue or reach out to the repository owner.

