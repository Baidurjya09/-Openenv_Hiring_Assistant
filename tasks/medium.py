"""
Medium task: Multiple reasonable candidates with partial overlaps.
"""

MEDIUM_TASK = {
    "task_id": "task_medium_001",
    "difficulty": "medium",
    "job_key": "job_medium_001",
    "resume_pool": "medium",
    # Emma (c_med_001) covers all required + TypeScript preferred
    # Iris (c_med_005) covers all required + Docker + AWS preferred
    # Both are strong fits; Frank and Grace are partial fits
    "correct_candidate_ids": ["c_med_001", "c_med_005"],
    "description": (
        "Select the best candidate(s) for a Full Stack Engineer role. "
        "Multiple candidates have partial overlaps — identify those who best satisfy "
        "both required and preferred skills."
    ),
}
