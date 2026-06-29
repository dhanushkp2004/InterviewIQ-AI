# AI Interview Prep Platform

A full-stack starter project for an AI Software Engineer Intern / Graduate AI Developer portfolio piece.

## What it does

- Supports lightweight user accounts for demo login
- Generates interview questions for AI/software roles
- Reviews candidate answers with structured feedback
- Scores resume text against a job description
- Persists sessions, feedback, and resume-match history in SQLite
- Shows a user dashboard with saved activity
- Runs in `demo mode` without an API key
- Supports OpenAI integration through the Responses API when `OPENAI_API_KEY` is configured

## Stack

- FastAPI
- Python
- Vanilla HTML/CSS/JavaScript frontend served by FastAPI
- Optional OpenAI API integration

## Quick start

1. Create and activate a virtual environment
2. Install dependencies:

```bash
pip install -r backend/requirements.txt
```

3. Copy the environment template:

```bash
copy backend\\.env.example backend\\.env
```

4. Run the app:

```bash
uvicorn backend.app.main:app --reload
```

5. Open:

`http://127.0.0.1:8000`

## Environment variables

- `OPENAI_API_KEY`: optional, enables live AI responses
- `OPENAI_MODEL`: optional, defaults to `gpt-4.1-mini`

If no API key is present, the app uses deterministic demo responses so the project still works locally.

## API endpoints

- `GET /api/health`
- `POST /api/auth/register`
- `POST /api/auth/login`
- `GET /api/job-description`
- `GET /api/dashboard/{user_id}`
- `POST /api/interview/session`
- `POST /api/interview/question`
- `POST /api/interview/feedback`
- `POST /api/resume/match`

## Project structure

```text
backend/
  app/
    services/
    static/
    main.py
    models.py
  requirements.txt
```

## Notes

This project is intentionally portfolio-friendly:

- clean code structure
- prompt-based AI features
- REST API design
- frontend + backend integration
- graceful fallback when external AI services are unavailable
