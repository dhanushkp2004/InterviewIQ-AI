from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from .database import Database
from .models import (
    AuthLoginRequest,
    AuthRegisterRequest,
    AuthResponse,
    DashboardResponse,
    HealthResponse,
    InterviewFeedbackRequest,
    InterviewFeedbackResponse,
    InterviewQuestionRequest,
    InterviewQuestionResponse,
    InterviewSessionCreate,
    InterviewSessionResponse,
    JobDescriptionResponse,
    ResumeMatchRequest,
    ResumeMatchResponse,
)
from .services.interview import select_question
from .services.llm import LLMService
from .services.scoring import calculate_match_score, extract_skill_matches

JOB_DESCRIPTION = """AI Software Engineer Intern / Graduate AI Developer

We are seeking a passionate Computer Science student or recent graduate to join our AI team as an AI Software Engineer Intern. The ideal candidate has a strong foundation in programming, an interest in Artificial Intelligence and Large Language Models (LLMs), and enjoys building intelligent applications that enhance user experiences."""

app = FastAPI(title="AI Interview Prep Platform")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/static", StaticFiles(directory="backend/app/static"), name="static")

llm_service = LLMService()
db = Database()


@app.get("/", include_in_schema=False)
async def root() -> FileResponse:
    return FileResponse("backend/app/static/index.html")


@app.get("/api/health", response_model=HealthResponse)
async def health() -> HealthResponse:
    return HealthResponse(status="ok", mode=llm_service.mode)


@app.post("/api/auth/register", response_model=AuthResponse)
async def register(payload: AuthRegisterRequest) -> AuthResponse:
    existing = db.get_user_by_email(payload.email)
    if existing:
        raise HTTPException(status_code=400, detail="Account already exists for this email.")
    try:
        user = db.create_user(payload.name, payload.email, payload.password)
    except Exception:
        raise HTTPException(status_code=400, detail="Unable to create account.")
    return AuthResponse(**user)


@app.post("/api/auth/login", response_model=AuthResponse)
async def login(payload: AuthLoginRequest) -> AuthResponse:
    user = db.authenticate_user(payload.email, payload.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid email or password.")
    return AuthResponse(**user)


@app.get("/api/job-description", response_model=JobDescriptionResponse)
async def job_description() -> JobDescriptionResponse:
    return JobDescriptionResponse(
        title="AI Software Engineer Intern / Graduate AI Developer",
        description=JOB_DESCRIPTION,
    )


@app.post("/api/interview/session", response_model=InterviewSessionResponse)
async def create_interview_session(payload: InterviewSessionCreate) -> InterviewSessionResponse:
    if not db.get_user(payload.user_id):
        raise HTTPException(status_code=404, detail="User not found.")
    session = db.create_session(payload.model_dump())
    return InterviewSessionResponse(
        session_id=session["id"],
        welcome_message=(
            f"Hi {payload.candidate_name}, your practice session for {payload.target_role} is ready."
        ),
    )


@app.post("/api/interview/question", response_model=InterviewQuestionResponse)
async def generate_question(payload: InterviewQuestionRequest) -> InterviewQuestionResponse:
    session = db.get_session(payload.session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Interview session not found.")

    question = select_question(
        seed=len(payload.session_id),
        focus_areas=session.get("focus_areas", []),
        include_follow_up=payload.include_follow_up,
    )
    db.update_session_question(payload.session_id, question["question"])
    return InterviewQuestionResponse(**question)


@app.post("/api/interview/feedback", response_model=InterviewFeedbackResponse)
async def generate_feedback(payload: InterviewFeedbackRequest) -> InterviewFeedbackResponse:
    session = db.get_session(payload.session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Interview session not found.")

    feedback = await llm_service.generate_feedback(payload.question, payload.answer)
    db.save_feedback(payload.session_id, payload.question, payload.answer, feedback)
    return InterviewFeedbackResponse(**feedback)


@app.post("/api/resume/match", response_model=ResumeMatchResponse)
async def score_resume(payload: ResumeMatchRequest) -> ResumeMatchResponse:
    job_description_text = payload.job_description or JOB_DESCRIPTION
    matched, missing = extract_skill_matches(payload.resume_text, job_description_text)
    score = calculate_match_score(matched, missing)

    recommendations = [
        "Add quantified project outcomes tied to AI or backend work.",
        "Highlight role-specific tools such as FastAPI, OpenAI APIs, and React.",
        "Show at least one project involving LLMs, NLP, or interview automation.",
    ]
    if missing:
        recommendations[0] = f"Close the gap on missing areas such as: {', '.join(missing[:4])}."

    response = ResumeMatchResponse(
        match_score=score,
        matched_skills=matched,
        missing_skills=missing,
        recommendations=recommendations,
    )
    if payload.user_id:
        if not db.get_user(payload.user_id):
            raise HTTPException(status_code=404, detail="User not found.")
        db.save_resume_match(
            payload.user_id,
            {
                "resume_text": payload.resume_text,
                "job_description": job_description_text,
            },
            response.model_dump(),
        )
    return response


@app.get("/api/dashboard/{user_id}", response_model=DashboardResponse)
async def dashboard(user_id: str) -> DashboardResponse:
    try:
        data = db.get_dashboard(user_id)
    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error))
    return DashboardResponse(**data)
