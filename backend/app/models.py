from typing import List, Optional

from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    status: str
    mode: str


class AuthRegisterRequest(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    email: str = Field(min_length=3, max_length=255)
    password: str = Field(min_length=4, max_length=100)


class AuthLoginRequest(BaseModel):
    email: str = Field(min_length=3, max_length=255)
    password: str = Field(min_length=4, max_length=100)


class AuthResponse(BaseModel):
    user_id: str
    name: str
    email: str


class JobDescriptionResponse(BaseModel):
    title: str
    description: str


class InterviewSessionCreate(BaseModel):
    user_id: str = Field(min_length=1)
    candidate_name: str = Field(min_length=1, max_length=100)
    target_role: str = Field(min_length=1, max_length=150)
    experience_level: str = Field(min_length=1, max_length=50)
    focus_areas: List[str] = Field(default_factory=list)


class InterviewSessionResponse(BaseModel):
    session_id: str
    welcome_message: str


class InterviewQuestionRequest(BaseModel):
    session_id: str
    include_follow_up: bool = True


class InterviewQuestionResponse(BaseModel):
    question: str
    category: str
    why_it_matters: str


class InterviewFeedbackRequest(BaseModel):
    session_id: str
    question: str
    answer: str = Field(min_length=1)


class InterviewFeedbackResponse(BaseModel):
    score: int
    strengths: List[str]
    improvements: List[str]
    sample_better_answer: str


class ResumeMatchRequest(BaseModel):
    user_id: Optional[str] = None
    resume_text: str = Field(min_length=1)
    job_description: Optional[str] = None


class ResumeMatchResponse(BaseModel):
    match_score: int
    matched_skills: List[str]
    missing_skills: List[str]
    recommendations: List[str]


class SessionHistoryItem(BaseModel):
    session_id: str
    candidate_name: str
    target_role: str
    experience_level: str
    focus_areas: List[str]
    created_at: str
    question_count: int
    last_question: Optional[str] = None


class FeedbackHistoryItem(BaseModel):
    session_id: str
    question: str
    answer: str
    score: int
    created_at: str


class ResumeMatchHistoryItem(BaseModel):
    match_score: int
    matched_skills: List[str]
    missing_skills: List[str]
    created_at: str


class DashboardResponse(BaseModel):
    user: AuthResponse
    sessions: List[SessionHistoryItem]
    feedback: List[FeedbackHistoryItem]
    resume_matches: List[ResumeMatchHistoryItem]
