# Newspaper Project

A Django based news website with user authentication, article management, and commenting features.

## Table of Contents

* [Features](#features)
* [Tech Stack](#tech-stack)
* [Quick Start](#quick-start)

  * [Option 1 Local Setup Virtual Environment](#option-1-local-setup-virtual-environment)
  * [Option 2 Docker Setup](#option-2-docker-setup)
* [Project Structure](#project-structure)
* [Key Models](#key-models)
* [URL Routes](#url-routes)
* [Testing](#testing)
* [Development](#development)
* [Deployment Considerations](#deployment-considerations)
* [Troubleshooting](#troubleshooting)
* [Contributing](#contributing)
* [License](#license)
* [Contact](#contact)

## Features

* **User Management**: Custom user model with registration, login, password reset, and birthday detection
* **Article CRUD**: Create, read, update, and delete articles with author only permissions
* **Commenting System**: Users can comment on articles (with restrictions)
* **Responsive UI**: Bootstrap 5 interface with modern design

## Tech Stack

* **Backend**: Python 3.12+, Django 5.2.7
* **Database**: PostgreSQL 18
* **Frontend**: Bootstrap 5, Crispy Forms
* **Containerization**: Docker & Docker Compose

## Quick Start

### Option 1 Local Setup Virtual Environment

#### Prerequisites

* Python 3.12.3+
* PostgreSQL 13+
* pip

#### Installation

1. **Clone and setup environment**

```bash
git clone https://github.com/peterkahumu/Newspaper-Project.git
cd newspaper_project
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

2. **Configure database**

```bash
# Create PostgreSQL database
psql -U postgres
CREATE DATABASE newspaper_db;
CREATE USER newspaper_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE newspaper_db TO newspaper_user;
\q
```

3. **Setup environment variables**

```bash
cp .env_example .env
# Edit .env with your settings
```

Example `.env`:

```env
DEBUG=True
SECRET_KEY=your-secret-key-here

DB_NAME=newspaper_db
DB_USER=newspaper_user
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
```

4. **Run migrations and create superuser**

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Visit: `http://127.0.0.1:8000`

---

### Option 2 Docker Setup

#### Prerequisites

* Docker Engine 20.10+
* Docker Compose 2.0+

#### Installation

1. **Clone and configure**

```bash
git clone https://github.com/peterkahumu/Newspaper-Project.git
cd newspaper_project
cp .env_example .env
# Edit .env - Set DB_HOST=db for Docker
```

2. **Build and run**

```bash
docker compose up -d --build
docker compose exec web python manage.py createsuperuser
```

Visit: `http://localhost:8000`

#### Docker Commands

```bash
# View logs
docker compose logs -f

# Stop containers
docker compose down

# Restart
docker compose restart

# Run migrations
docker compose exec web python manage.py migrate

# Access shell
docker compose exec web python manage.py shell
```

## Project Structure

```
newspaper_project/
├── accounts/              # User authentication
├── articles/              # Article & comment management
├── pages/                 # Static pages
├── templates/             # HTML templates
├── newspaper_project/     # Project settings
├── requirements.txt       # Python dependencies
├── Dockerfile             # Docker configuration
└── docker-compose.yml     # Docker Compose setup
```

## Key Models

### CustomUser

* UUID primary key
* Additional fields: date_of_birth
* Computed properties: age, is_birthday

### Article

* UUID primary key
* Fields: title, body, author, created_at, updated_at
* Snippet property (first 5 words)
* Author only edit/delete permissions

### Comment

* UUID primary key
* Restrictions: No self commenting, one comment per article per user

## URL Routes

| URL                          | Description                  | Auth Required |
| ---------------------------- | ---------------------------- | ------------- |
| `/`                          | Homepage                     | No            |
| `/accounts/register/`        | User registration            | No            |
| `/accounts/login/`           | User login                   | No            |
| `/accounts/logout/`          | User logout                  | Yes           |
| `/accounts/password_change/` | Change password              | Yes           |
| `/accounts/password_reset/`  | Reset password               | No            |
| `/articles/`                 | List all articles            | Yes           |
| `/articles/new/`             | Create article               | Yes           |
| `/articles/<uuid>/`          | View article & comments      | Yes           |
| `/articles/<uuid>/edit/`     | Edit article (author only)   | Yes           |
| `/articles/<uuid>/delete/`   | Delete article (author only) | Yes           |

## Testing

```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test accounts
python manage.py test articles

# With Docker
docker compose exec web python manage.py test
```

## Development

### Code Formatting

```bash
# Format code with Black
black .

# Check formatting
black --check .
```

### Database Operations

```bash
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Access admin
# Visit http://localhost:8000/admin/
```

### Adding Dependencies

```bash
pip install package-name
pip freeze > requirements.txt

# For Docker, rebuild
docker compose up --build
```

## Deployment Considerations

**Before deploying to production:**

1. Set `DEBUG = False` in settings
2. Configure `ALLOWED_HOSTS` with your domain
3. Use strong `SECRET_KEY` (generate new one)
4. Set up production database
5. Configure HTTPS/SSL
6. Run `python manage.py collectstatic`
7. Use production WSGI server (Gunicorn)
8. Set up NGINX as reverse proxy
9. Configure email backend for password reset
10. Enable security headers in settings

**Example production settings:**

```python
DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com']
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
```

## Troubleshooting

**Template not found**: Check `TEMPLATES['DIRS']` includes templates folder

**Database connection error**: Verify PostgreSQL is running and credentials in `.env`

**Port already in use**: Kill process on port 8000 or use different port

**Migration conflicts**: Delete migrations (except `__init__.py`), recreate database, run migrations

**Docker permission issues**: Run `chmod +x wait-for-it.sh`

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feat/my-feature`
3. Make changes and write tests
4. Run tests: `python manage.py test`
5. Format code: `black .`
6. Commit: `git commit -m "Add my feature"`
7. Push: `git push origin feat/my-feature`
8. Open a Pull Request

## License

This project is licensed under the MIT License see the [LICENSE](LICENSE) file for details.

## Contact

For questions or issues, please open an issue on GitHub or contact the repository owner.
