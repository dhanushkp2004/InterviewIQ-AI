import json
import os
from typing import Any, Dict, List

import httpx


class LLMService:
    def __init__(self) -> None:
        self.api_key = os.getenv("OPENAI_API_KEY", "").strip()
        self.model = os.getenv("OPENAI_MODEL", "gpt-4.1-mini").strip()

    @property
    def mode(self) -> str:
        return "openai" if self.api_key else "demo"

    async def generate_feedback(self, question: str, answer: str) -> Dict[str, Any]:
        if not self.api_key:
            return self._demo_feedback(question, answer)

        prompt = (
            "You are an interview coach for an AI software engineer intern role. "
            "Return strict JSON with keys: score, strengths, improvements, sample_better_answer. "
            "score must be an integer from 0 to 100. strengths and improvements must be arrays of short strings."
        )
        user_input = f"Question: {question}\nCandidate answer: {answer}"

        try:
            payload = {
                "model": self.model,
                "input": [
                    {"role": "developer", "content": [{"type": "input_text", "text": prompt}]},
                    {"role": "user", "content": [{"type": "input_text", "text": user_input}]},
                ],
            }
            async with httpx.AsyncClient(timeout=20.0) as client:
                response = await client.post(
                    "https://api.openai.com/v1/responses",
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json",
                    },
                    json=payload,
                )
                response.raise_for_status()
                data = response.json()
        except Exception:
            return self._demo_feedback(question, answer)

        text = self._extract_output_text(data)
        try:
            parsed = json.loads(text)
            return {
                "score": max(0, min(100, int(parsed.get("score", 70)))),
                "strengths": list(parsed.get("strengths", []))[:4],
                "improvements": list(parsed.get("improvements", []))[:4],
                "sample_better_answer": str(parsed.get("sample_better_answer", "")),
            }
        except Exception:
            return self._demo_feedback(question, answer)

    def _extract_output_text(self, data: Dict[str, Any]) -> str:
        if isinstance(data.get("output_text"), str) and data["output_text"].strip():
            return data["output_text"]

        outputs = data.get("output", [])
        chunks: List[str] = []
        for item in outputs:
            for content in item.get("content", []):
                text = content.get("text")
                if text:
                    chunks.append(text)
        return "\n".join(chunks)

    def _demo_feedback(self, question: str, answer: str) -> Dict[str, Any]:
        answer_lower = answer.lower()
        score = 55
        if len(answer.split()) > 80:
            score += 12
        if any(term in answer_lower for term in ["fastapi", "python", "api", "testing", "prompt"]):
            score += 14
        if any(term in answer_lower for term in ["tradeoff", "scalable", "error handling", "monitoring"]):
            score += 12
        score = min(score, 92)

        return {
            "score": score,
            "strengths": [
                "Shows role-relevant technical awareness.",
                "Connects ideas to implementation rather than staying purely theoretical.",
                "Demonstrates motivation for AI product development.",
            ],
            "improvements": [
                "Add a more concrete example from a project or coursework.",
                "Explain technical tradeoffs more explicitly.",
                "Mention testing, evaluation, or monitoring considerations.",
            ],
            "sample_better_answer": (
                f"For '{question}', I would give a structured answer that explains the architecture, "
                "implementation choices, tradeoffs, and how I would validate the result in production."
            ),
        }
