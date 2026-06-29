import hashlib
import json
import sqlite3
from pathlib import Path
from uuid import uuid4


BASE_DIR = Path("backend/data")
DB_PATH = BASE_DIR / "app.db"


class Database:
    def __init__(self) -> None:
        BASE_DIR.mkdir(parents=True, exist_ok=True)
        self._initialize()

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(DB_PATH)
        connection.row_factory = sqlite3.Row
        return connection

    def _initialize(self) -> None:
        with self._connect() as connection:
            connection.executescript(
                """
                CREATE TABLE IF NOT EXISTS users (
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    email TEXT NOT NULL UNIQUE,
                    password_hash TEXT NOT NULL,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                );

                CREATE TABLE IF NOT EXISTS sessions (
                    id TEXT PRIMARY KEY,
                    user_id TEXT NOT NULL,
                    candidate_name TEXT NOT NULL,
                    target_role TEXT NOT NULL,
                    experience_level TEXT NOT NULL,
                    focus_areas TEXT NOT NULL,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    question_count INTEGER DEFAULT 0,
                    last_question TEXT,
                    FOREIGN KEY(user_id) REFERENCES users(id)
                );

                CREATE TABLE IF NOT EXISTS feedback (
                    id TEXT PRIMARY KEY,
                    session_id TEXT NOT NULL,
                    question TEXT NOT NULL,
                    answer TEXT NOT NULL,
                    score INTEGER NOT NULL,
                    strengths TEXT NOT NULL,
                    improvements TEXT NOT NULL,
                    sample_better_answer TEXT NOT NULL,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY(session_id) REFERENCES sessions(id)
                );

                CREATE TABLE IF NOT EXISTS resume_matches (
                    id TEXT PRIMARY KEY,
                    user_id TEXT NOT NULL,
                    resume_text TEXT NOT NULL,
                    job_description TEXT NOT NULL,
                    match_score INTEGER NOT NULL,
                    matched_skills TEXT NOT NULL,
                    missing_skills TEXT NOT NULL,
                    recommendations TEXT NOT NULL,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY(user_id) REFERENCES users(id)
                );
                """
            )

    def _hash_password(self, password: str) -> str:
        return hashlib.sha256(password.encode("utf-8")).hexdigest()

    def create_user(self, name: str, email: str, password: str) -> dict:
        user = {
            "id": str(uuid4()),
            "name": name,
            "email": email.lower().strip(),
            "password_hash": self._hash_password(password),
        }
        with self._connect() as connection:
            connection.execute(
                "INSERT INTO users (id, name, email, password_hash) VALUES (?, ?, ?, ?)",
                (user["id"], user["name"], user["email"], user["password_hash"]),
            )
        return {"user_id": user["id"], "name": user["name"], "email": user["email"]}

    def get_user_by_email(self, email: str) -> dict | None:
        with self._connect() as connection:
            row = connection.execute(
                "SELECT id, name, email FROM users WHERE email = ?",
                (email.lower().strip(),),
            ).fetchone()
        if not row:
            return None
        return {"user_id": row["id"], "name": row["name"], "email": row["email"]}

    def authenticate_user(self, email: str, password: str) -> dict | None:
        with self._connect() as connection:
            row = connection.execute(
                "SELECT id, name, email, password_hash FROM users WHERE email = ?",
                (email.lower().strip(),),
            ).fetchone()
        if not row:
            return None
        if row["password_hash"] != self._hash_password(password):
            return None
        return {"user_id": row["id"], "name": row["name"], "email": row["email"]}

    def get_user(self, user_id: str) -> dict | None:
        with self._connect() as connection:
            row = connection.execute(
                "SELECT id, name, email FROM users WHERE id = ?",
                (user_id,),
            ).fetchone()
        if not row:
            return None
        return {"user_id": row["id"], "name": row["name"], "email": row["email"]}

    def create_session(self, payload: dict) -> dict:
        session = {
            "id": str(uuid4()),
            "user_id": payload["user_id"],
            "candidate_name": payload["candidate_name"],
            "target_role": payload["target_role"],
            "experience_level": payload["experience_level"],
            "focus_areas": json.dumps(payload.get("focus_areas", [])),
        }
        with self._connect() as connection:
            connection.execute(
                """
                INSERT INTO sessions (id, user_id, candidate_name, target_role, experience_level, focus_areas)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    session["id"],
                    session["user_id"],
                    session["candidate_name"],
                    session["target_role"],
                    session["experience_level"],
                    session["focus_areas"],
                ),
            )
        return session

    def get_session(self, session_id: str) -> dict | None:
        with self._connect() as connection:
            row = connection.execute("SELECT * FROM sessions WHERE id = ?", (session_id,)).fetchone()
        if not row:
            return None
        data = dict(row)
        data["focus_areas"] = json.loads(data["focus_areas"])
        return data

    def update_session_question(self, session_id: str, question: str) -> None:
        with self._connect() as connection:
            connection.execute(
                """
                UPDATE sessions
                SET question_count = question_count + 1, last_question = ?
                WHERE id = ?
                """,
                (question, session_id),
            )

    def save_feedback(self, session_id: str, question: str, answer: str, feedback: dict) -> None:
        with self._connect() as connection:
            connection.execute(
                """
                INSERT INTO feedback (
                    id, session_id, question, answer, score, strengths, improvements, sample_better_answer
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    str(uuid4()),
                    session_id,
                    question,
                    answer,
                    feedback["score"],
                    json.dumps(feedback["strengths"]),
                    json.dumps(feedback["improvements"]),
                    feedback["sample_better_answer"],
                ),
            )

    def save_resume_match(self, user_id: str, payload: dict, response: dict) -> None:
        with self._connect() as connection:
            connection.execute(
                """
                INSERT INTO resume_matches (
                    id, user_id, resume_text, job_description, match_score, matched_skills, missing_skills, recommendations
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    str(uuid4()),
                    user_id,
                    payload["resume_text"],
                    payload["job_description"],
                    response["match_score"],
                    json.dumps(response["matched_skills"]),
                    json.dumps(response["missing_skills"]),
                    json.dumps(response["recommendations"]),
                ),
            )

    def get_dashboard(self, user_id: str) -> dict:
        user = self.get_user(user_id)
        if not user:
            raise ValueError("User not found.")

        with self._connect() as connection:
            session_rows = connection.execute(
                """
                SELECT id, candidate_name, target_role, experience_level, focus_areas, created_at, question_count, last_question
                FROM sessions
                WHERE user_id = ?
                ORDER BY datetime(created_at) DESC
                """,
                (user_id,),
            ).fetchall()
            feedback_rows = connection.execute(
                """
                SELECT f.session_id, f.question, f.answer, f.score, f.created_at
                FROM feedback f
                JOIN sessions s ON s.id = f.session_id
                WHERE s.user_id = ?
                ORDER BY datetime(f.created_at) DESC
                LIMIT 10
                """,
                (user_id,),
            ).fetchall()
            match_rows = connection.execute(
                """
                SELECT match_score, matched_skills, missing_skills, created_at
                FROM resume_matches
                WHERE user_id = ?
                ORDER BY datetime(created_at) DESC
                LIMIT 10
                """,
                (user_id,),
            ).fetchall()

        sessions = []
        for row in session_rows:
            item = dict(row)
            item["session_id"] = item.pop("id")
            item["focus_areas"] = json.loads(item["focus_areas"])
            sessions.append(item)

        feedback = [dict(row) for row in feedback_rows]

        resume_matches = []
        for row in match_rows:
            item = dict(row)
            item["matched_skills"] = json.loads(item["matched_skills"])
            item["missing_skills"] = json.loads(item["missing_skills"])
            resume_matches.append(item)

        return {
            "user": user,
            "sessions": sessions,
            "feedback": feedback,
            "resume_matches": resume_matches,
        }
