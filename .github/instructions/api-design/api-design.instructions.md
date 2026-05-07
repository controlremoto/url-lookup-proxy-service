---
name: 'Python Standards'
description: 'Coding conventions for Python files'
applyTo: '**/*.py'
---

# **INSTRUCTIONS.md — Python Project Technical Guidelines**

These instructions define the coding, formatting, documentation, testing, and architectural standards for this Python project.  
They ensure consistency, readability, maintainability, and alignment with **PEP 8 – Style Guide for Python Code**.   [peps.python.org](https://peps.python.org/pep-0008/)

---

## **1. Code Style (PEP 8 Compliance)**

### **1.1 Indentation & Layout**
- Always import modules before using their functions or attributes in your code.
- Use **4 spaces per indentation level** (never tabs).   [peps.python.org](https://peps.python.org/pep-0008/)  
- Maximum line length: **79 characters** for code, **72 characters** for docstrings/comments.  
- Use **implicit line joining** inside parentheses/brackets/braces when breaking long lines.  
- Keep top‑level function and class definitions separated by **two blank lines**.

### **1.2 Naming Conventions**
- **Variables & functions**: `snake_case`  
- **Classes**: `CapWords` (CamelCase)  
- **Constants**: `UPPER_SNAKE_CASE`  
- **Modules**: short, lowercase names  
- **Packages**: lowercase, no underscores  
These conventions follow PEP 8 naming rules.   [Real Python](https://realpython.com/python-pep8/)

### **1.3 Imports**
- Place imports at the **top of the file**.  
- Group imports in this order:  
  1. Standard library  
  2. Third‑party libraries  
  3. Local application imports  
- Avoid wildcard imports (`from module import *`).  
- Use one import per line.

### **1.4 Whitespace Rules**
- Surround binary operators with **one space**:  
  `x = a + b`  
- No spaces inside parentheses, brackets, or before commas:  
  `func(a, b)` not `func( a , b )`  
- No trailing whitespace.

---

## **2. Documentation Standards**

### **2.1 Docstrings**
- Use **triple‑quoted** docstrings (`""" """`) for:
  - Modules  
  - Classes  
  - Public functions/methods  
- Follow **PEP 257** conventions.  
- Docstring format:  
  - Short summary line  
  - Blank line  
  - Detailed explanation (optional)  
  - Args / Returns / Raises sections (Google or NumPy style allowed)

### **2.2 Comments**
- Keep comments **up‑to‑date** and meaningful.  
- Use inline comments sparingly.  
- Block comments should explain *why*, not *what*.

---

## **3. Project Structure**

```
project/
│── src/
│   └── <package>/
│       ├── __init__.py
│       ├── api/
│       ├── db/
│       ├── models/
│       ├── services/
│       └── utils/
│
│── tests/
│── requirements.txt / pyproject.toml
│── Dockerfile
│── docker-compose.yml
│── README.md
│── INSTRUCTIONS.md
```

---

## **4. Error Handling & Logging**

### **4.1 Error Handling**
- Never swallow exceptions silently.  
- Raise specific exceptions (`ValueError`, `KeyError`, etc.).  
- Wrap external calls (DB, HTTP, filesystem) with safe error handling.

### **4.2 Logging**
- Use Python’s built‑in `logging` module.  
- Log levels:
  - `DEBUG` for development  
  - `INFO` for normal operations  
  - `WARNING` for recoverable issues  
  - `ERROR` for failures  
  - `CRITICAL` for system‑level errors  
- No `print()` statements in production code.

---

## **5. Testing Requirements**

### **5.1 Test Framework**
- Use **pytest**.  
- Minimum coverage target: **80%**.  
- Tests must be deterministic and isolated.

### **5.2 Test Structure**
```
tests/
│── unit/
│── integration/
│── fixtures/
```

### **5.3 What to Test**
- API endpoints  
- Database interactions  
- Business logic  
- Error handling  
- Edge cases

---

## **6. Database Guidelines**

- Use SQLite for local development unless otherwise specified.  
- Use migrations (e.g., Alembic) when using SQL databases.  
- Keep DB access inside a dedicated `db/` or `repository/` layer.  
- Avoid embedding SQL directly in business logic.

---

## **7. API Development Standards**

- Use FastAPI or Flask for HTTP services.  
- Validate all input (FastAPI’s Pydantic models recommended).  
- Return consistent JSON responses:
  - `data`
  - `error`
  - `meta` (optional)
- Use proper HTTP status codes.

---

## **8. Dependency Management**

- Use `requirements.txt` or `pyproject.toml`.  
- Pin versions for production builds.  
- Avoid unnecessary dependencies.  
- Run `pip-audit` or similar tools to check vulnerabilities.

---

## **9. Containerization**

- Provide a **Dockerfile** that:
  - Uses a slim Python base image  
  - Installs dependencies efficiently  
  - Runs the app with a production server (e.g., `uvicorn` or `gunicorn`)  
- Provide a `docker-compose.yml` for local development.

---

## **10. CI/CD Expectations**

- Run tests on every PR.  
- Enforce linting with:
  - `flake8` or `ruff`  
  - `black` for formatting  
  - `isort` for import ordering  
- Block merges if tests or linting fail.

---

## **11. Security Practices**

- Never commit secrets.  
- Use environment variables for configuration.  
- Validate all external input.  
- Keep dependencies updated.

---

## **12. Performance & Scalability**

- Prefer async frameworks (FastAPI) when appropriate.  
- Cache expensive operations (Redis recommended).  
- Avoid premature optimization—measure first.

---

## **13. Git Workflow**

- Use meaningful commit messages.  
- Follow feature‑branch workflow:
  - `main` → stable  
  - `dev` → integration  
  - `feature/*` → new work  
- PRs must include:
  - Description  
  - Tests  
  - Lint‑clean code  

---

## **14. Code Review Checklist**

Before submitting code, ensure:

- Code follows PEP 8.  
- No unused imports or variables.  
- Functions are small and single‑purpose.  
- Tests pass locally.  
- Documentation is updated.  
- Logging is appropriate.  
