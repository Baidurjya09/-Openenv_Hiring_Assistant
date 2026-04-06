"""
Hard task: Very similar candidates requiring reasoning over skills + experience.
"""

HARD_TASK = {
    "task_id": "task_hard_001",
    "difficulty": "hard",
    "job_key": "job_hard_001",
    "resume_pool": "hard",
    # Jack (c_hard_001): all required + Kubernetes + CUDA — strongest fit
    # Karen (c_hard_002): all required + LLMs + Spark — strong fit
    # Leo (c_hard_003): uses TensorFlow not PyTorch, meets minimum bar
    # Mia (c_hard_004): missing MLOps — disqualified on required skill
    # Nathan (c_hard_005): no deep learning or MLOps — disqualified
    "correct_candidate_ids": ["c_hard_001", "c_hard_002"],
    "description": (
        "Select the best candidate(s) for a Senior ML Engineer role. "
        "Candidates are very similar — requires careful reasoning over required skills, "
        "preferred skills, and years of experience."
    ),
}
