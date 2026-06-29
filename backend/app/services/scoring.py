from typing import List


CORE_SKILLS = [
    "python",
    "fastapi",
    "react",
    "javascript",
    "html",
    "css",
    "rest api",
    "json",
    "git",
    "github",
    "openai",
    "llm",
    "prompt engineering",
    "nlp",
    "rag",
    "docker",
    "aws",
    "azure",
    "google cloud",
    "ci/cd",
]


def extract_skill_matches(resume_text: str, job_description: str) -> tuple[List[str], List[str]]:
    combined_resume = resume_text.lower()
    combined_job = job_description.lower()

    relevant_skills = [skill for skill in CORE_SKILLS if skill in combined_job]
    if not relevant_skills:
        relevant_skills = CORE_SKILLS[:10]

    matched = [skill for skill in relevant_skills if skill in combined_resume]
    missing = [skill for skill in relevant_skills if skill not in combined_resume]
    return matched, missing


def calculate_match_score(matched: List[str], missing: List[str]) -> int:
    total = len(matched) + len(missing)
    if total == 0:
        return 50
    return round((len(matched) / total) * 100)
