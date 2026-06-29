from typing import List


QUESTION_BANK = [
    {
        "category": "Python",
        "question": "How would you structure a FastAPI service for an AI interview platform so it stays maintainable as features grow?",
        "why_it_matters": "This checks backend design, API thinking, and code organization.",
    },
    {
        "category": "LLMs",
        "question": "What prompt engineering techniques would you use to improve consistency in an AI interview assistant?",
        "why_it_matters": "This measures practical LLM understanding beyond theory.",
    },
    {
        "category": "Frontend",
        "question": "How would you build a responsive interview practice dashboard for desktop and mobile users?",
        "why_it_matters": "This evaluates product thinking and frontend execution.",
    },
    {
        "category": "APIs",
        "question": "What error handling patterns would you add when integrating an external AI API into a production application?",
        "why_it_matters": "This reveals reliability and real-world engineering judgment.",
    },
    {
        "category": "System Design",
        "question": "How would you design a resume-to-job match scorer that is fast, explainable, and easy to improve over time?",
        "why_it_matters": "This shows problem decomposition and AI product design ability.",
    },
]


def select_question(seed: int, focus_areas: List[str], include_follow_up: bool) -> dict:
    base = QUESTION_BANK[seed % len(QUESTION_BANK)].copy()
    if focus_areas:
        chosen_focus = focus_areas[seed % len(focus_areas)]
        base["question"] += f" Please relate your answer to {chosen_focus}."
    if include_follow_up:
        base["why_it_matters"] += " A strong answer should include tradeoffs and implementation details."
    return base
