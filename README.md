# Expense Tracker API

[![Day 5](https://img.shields.io/badge/Day%205-30_days_30_projects-blue)](https://github.com/Valent-p/30-days-30-projects-sep26)

A simple expense tracker API built with FastAPI and SQLite for recording and viewing today's expenses.

## Features

- Add expenses with amount, category, and description
- List today's expenses
- Daily summary (total spent, breakdown by category)
- Update and delete expenses
- Vanilla JS frontend with Material Icons
- Sharp, dark-themed UI with skyblue accent

## Project Structure

```
expense-tracker/
├── main.py             # FastAPI app with SQLite + CRUD endpoints
├── requirements.txt
├── expenses.db         # SQLite database (auto-created)
├── run.sh              # Quick start script
└── frontend/
    ├── index.html      # Expense tracker UI
    ├── style.css       # Dark theme with skyblue accents
    └── app.js          # Frontend API client
```

## Setup

### Create and activate a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Run the server

```bash
./run.sh
```

Or manually:

```bash
uvicorn main:app --reload --port 8000
```

Open `http://localhost:8000` in your browser.

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/expenses` | List today's expenses |
| POST | `/api/expenses` | Create a new expense |
| PUT | `/api/expenses/{id}` | Update an expense |
| DELETE | `/api/expenses/{id}` | Delete an expense |
| GET | `/api/expenses/summary` | Daily spending summary |

## Day 5 - 30 Days, 30 Projects

This is the 5th project in the [30 Days, 30 Projects](https://github.com/Valent-p/30-days-30-projects-sep26) challenge.
