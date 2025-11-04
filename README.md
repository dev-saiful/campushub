# CampusHub — University Management API

CampusHub is a modular FastAPI backend that demonstrates a practical university management system for:

- Students
- Teachers
- Courses
- Class routines
- Bus schedules
- Generated PDFs (reports & schedules)

This repository is designed as a learning scaffold to show how to build a production-like FastAPI service with authentication, persistence, file handling and containerization.

## Key Features

- FastAPI + ASGI
- SQLModel / SQLAlchemy with PostgreSQL
- JWT authentication (login / protected endpoints)
- CRUD APIs for students, teachers, courses, routines, buses
- File uploads and PDF generation endpoints
- Docker-ready (Dockerfile / docker-compose)
- Unit tests and OpenAPI (Swagger) documentation

## 🧱 Project Architecture

```
campushub/
│
├── app/
│   ├── main.py
│   ├── core/        # Configs (DB, JWT, env)
│   ├── models/      # Database models
│   ├── schemas/     # Pydantic schemas
│   ├── routes/      # Routers (student, teacher, auth, etc.)
│   ├── services/    # Business logic
│   ├── utils/       # Helper functions (pdf, jwt, etc.)
│   └── tests/       # Unit tests
│
├── Dockerfile
├── docker-compose.yml
├── .env
├── requirements.txt
└── README.md
```

## Quickstart (development)

1. Clone the repo

   git clone <repo-url>
   cd campushub

2. Create a Python virtual environment and install dependencies

   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt

3. Configure environment variables (example .env)

   - DATABASE_URL=postgresql://user:pass@localhost:5432/campushub
   - SECRET_KEY=<your-jwt-secret>
   - OTHER_SETTINGS...

4. Run the app (development)

   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

5. Open API docs

   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

## Database

- Uses PostgreSQL in production examples.
- Migrations supported via Alembic (if included).
- For local development you can use Docker Compose to start a DB.

## Docker

To run with Docker Compose (example):

1. docker compose up --build
2. The API will be available at http://localhost:8000

(Adjust docker-compose.yml and environment variables as needed.)

## Authentication

- JWT-based auth for protected endpoints.
- Endpoints: register, login -> receive access token -> use in Authorization: Bearer <token> header.

## File Uploads & PDF Generation

- Endpoints for uploading files (e.g., images, attachments).
- API routes to generate PDFs (schedules, reports) and return as downloadable files.

## Testing

- Unit tests located in tests/.
- Run tests with pytest:

  pytest -q

## Contributing

- Create issues for bugs or feature requests.
- Open pull requests with clear descriptions and tests.

## License

Specify your license here (e.g., MIT).

## Contact

For questions, open an issue or PR in the repository.
