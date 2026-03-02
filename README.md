# Taskify - Professional To-Do Application API & Web Platform

Taskify is a robust, production-ready Full-Stack Python web application and scalable RESTful API built on the Flask ecosystem. 

Designed iteratively across 9 comprehensive engineering phases, this project demonstrates advanced concepts in backend application factory architecture, stateful Session authentication, stateless JWT security, SQL relational modeling, dynamic frontend integrations, and deployment-ready WSGI scaling.

## 🚀 Features

### Core Task Management
- **Full CRUD Operations**: Create, Read, Update, and Delete personalized tasks natively.
- **Dynamic Scoping**: Stringent authorization logic ensuring users can strictly view and mutate only their underlying tasks.
- **Rich Task Metadata**: Support for tracking Priority Levels (Low, Medium, High), State (Pending, In-Progress, Completed), and calendar-bound Due Dates.
- **Client-Side Reactivity**: Vanilla JavaScript integrations that dynamically interpret due dates, instantly injecting warning UI components ("Overdue") onto cards directly inside the DOM without roundtripping to the server.

### Robust Security & Authentication
- **Dual Authentication Paradigms**: 
  - Validated Session-Cookie architecture (`Flask-Login`) serving the frontend.
  - Authorized JSON Web Tokens (JWT) natively serving the decoupled JSON API (`Flask-JWT-Extended`).
- **Cryptographic Hashing**: Secure storage of user passwords leveraged by Werkzeug's `pbkdf2:sha256` iterations.
- **CSRF Defense**: Omni-present Cross-Site Request Forgery (`Flask-WTF`) tokens meticulously injected against all state-mutating HTML forms.
- **Rate-Limiting (DDoS Protection)**: Throttled ingress pipelines (`Flask-Limiter`) enforcing strict API threshold boundaries on Authentication endpoints (e.g., 5 min/attempts for Registration).
- **HTTP Security Headers**: Automated `Flask-Talisman` integration injecting rigorous modern browser protections (HSTS, nosniff, frame-deny) solely in production.
- **Parametrized Execution**: Complete SQL Injection immunity implicitly inherited via SQLAlchemy's abstract ORM transaction building.
- **Password Complexity Validation**: Form logic blocking weak entropy combinations natively upon registration.

### Professional UI/UX
- Responsive **Bootstrap 5** component framework.
- Themed custom CSS UI components incorporating dynamic shadows, modern gradients, and border-radios paradigms.
- Integrated **Flash Notifications** providing immediate visual feedback on API transactions.
- Interactive JavaScript modal confirmations preventing accidental cascade deletions.

### Standalone REST JSON API
- A fully decoupled API blueprint (`/api/*`) resolving strict JSON payloads explicitly for mobile apps or remote client consumption.
- `/api/login` payload exchanging standard credentials for authorized Bearer Tokens.
- Native API CRUD mappings returning explicit REST Status codes (200, 201, 401, 403, 404, 422).

### Testing & Quality Assurance
- Advanced `pytest` suites (`test_flows.py`, `test_api.py`) simulating comprehensive e2e workflows.
- Modularized fixtures leveraging isolated in-memory test databases (`sqlite:///test_todo.db`) and CSRF exemptions to rigorously exercise endpoint authorization logic natively.

---

## 🏗 System Architecture

The project has evolved from a monolithic script into a modern **Application Factory Pattern**.

```
todo-app/
│
├── app/                        # Main Application Package
│   ├── __init__.py             # App Factory & Extension Initialization
│   ├── models.py               # SQLAlchemy Relational Models (Database Layer)
│   ├── routes.py               # Frontend Web Blueprint (Session Auth)
│   ├── api.py                  # Headless REST Blueprint (JWT Auth)
│   ├── static/                 # Custom CSS / JS assets
│   └── templates/              # Jinja2 HTML Views
│
├── tests/                      # Pytest Verification Suites
│   ├── conftest.py             # App Fixtures & Test DB configurations
│   ├── test_flows.py           # Authentication & Isolation web assertions
│   └── test_api.py             # JWT Bearer token API assertions
│
├── app.py                      # Main entry point hook (WSGI runtime)
├── gunicorn_config.py          # Scalable production server definitions
├── Dockerfile                  # Container instructions
├── requirements.txt            # Python dependencies
└── .env.example                # Environment variable templating
```

This structural paradigm provides extreme modularity:
1. **Blueprints (`routes` vs `api`)**: By isolating the API logic from the Jinja Rendering logic, the application flawlessly supports Headless Clients (Mobile apps) and standard Web Browsers simultaneously without code overlap.
2. **App Factory (`create_app()`)**: Instantiating the app via a function allows continuous overriding of configurations (`.env`) inherently critical for Test Isolation and Production deployments. 

---

## 🗄 Database Schema Description

The application relies on a strictly relational SQL schema managed seamlessly via the `Flask-SQLAlchemy` ORM.

### 1. `User` Table (Model)
- Operates as the parent entity representing an authenticated human identity.
- Handles cryptographic storage and natively supports the `UserMixin` required by `Flask-Login` session management.
- **Relationships**: Maintains a `db.relationship` linking `1 -> Many` descending Tasks, enforcing cascading data models.

### 2. `Todo` Table (Model)
- Operates as the child entity representing an isolated unit of work.
- **Foreign Key**: Subservient to the `User` table by storing the `user_id`, guaranteeing authoritative ownership (which the Routes explicitly validate against `current_user.id`).
- Contains flexible columns: `Priority` maps, `Complete` boolean toggles, and nullable `due_date` parameters explicitly mapped to standard `datetime` objects.

*(Note: Advanced SaaS expansions—Teams, Notifications, Comments—require complex association tables effectively designed in Phase 10 conceptual architecture, necessitating Migration pipelines to evolve the Foreign Key relationships safely).*

---

## 🚀 Deployment Instructions

This application is strictly parameterized through Operating System Environments. *You should never hardcode credentials into the logic.*

### Local Development / Evaluation
1. Clone the repository natively locally.
2. Initialize virtual environment: `python -m venv venv` and activate it.
3. Install strict dependencies: `pip install -r requirements.txt`.
4. Create a local `.env` file explicitly defining your logic:
   ```env
   FLASK_ENV=development
   SECRET_KEY=long-random-string-for-sessions
   JWT_SECRET_KEY=another-random-string-for-tokens
   DATABASE_URL=sqlite:///todo.db
   ```
5. Ignite the local development server natively: `python app.py`.
6. Alternatively, execute the comprehensive test suite to verify module behavior: `python -m pytest tests/ -v`.

### Production Server (Render / Docker)
The application has been outfitted sequentially for horizontal scaling via Docker and Gunicorn.

1. Inject the `.env` variables physically into your hosting provider's Secrets interface. Ensure `FLASK_ENV=production`. (This natively triggers `Talisman` secure headers and aborts the interactive `werkzeug` debugger).
2. Override SQLite with a production PostgreSQL connection string into `DATABASE_URL`.
3. The platform will automatically execute the contained `Dockerfile`, which exposes port `10000`, delegates execution natively to `gunicorn`, and leverages the optimized Thread geometries written inside `gunicorn_config.py` explicitly for Web Concurrency.


