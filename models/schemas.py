from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional


class JobDescription(BaseModel):
    id: str
    title: str
    required_skills: List[str]
    preferred_skills: List[str]
    min_experience_years: int
    description: str


class Candidate(BaseModel):
    id: str
    name: str
    skills: List[str]
    experience_years: int
    summary: str


class Observation(BaseModel):
    job_description: Dict[str, Any]
    resumes: List[Dict[str, Any]]
    task_id: str
    difficulty: str


class Action(BaseModel):
    selected_candidates: List[str] = Field(
        ..., description="List of candidate IDs selected for the role"
    )


class Reward(BaseModel):
    score: float = Field(..., ge=0.0, le=1.0)
    correct_selections: int
    total_correct: int
    false_positives: int
    feedback: str


class StepResult(BaseModel):
    observation: Observation
    reward: Reward
    done: bool
    info: Dict[str, Any]
